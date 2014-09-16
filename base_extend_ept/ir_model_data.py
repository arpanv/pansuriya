import logging
import re
import time
import types

import openerp
import openerp.modules.registry
from openerp import SUPERUSER_ID
from openerp import netsvc, pooler, tools
from openerp.osv import fields,osv
from openerp.osv.orm import Model
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools import config
from openerp.tools.translate import _
from openerp.osv.orm import except_orm, browse_record
_logger = logging.getLogger(__name__)
MODULE_UNINSTALL_FLAG = '_force_unlink'

class ir_model_data_ext(osv.osv):
    _inherit = 'ir.model.data'
    
    def _module_data_uninstall(self, cr, uid, modules_to_remove, context=None):
        """Deletes all the records referenced by the ir.model.data entries
        ``ids`` along with their corresponding database backed (including
        dropping tables, columns, FKs, etc, as long as there is no other
        ir.model.data entry holding a reference to them (which indicates that
        they are still owned by another module). 
        Attempts to perform the deletion in an appropriate order to maximize
        the chance of gracefully deleting all records.
        This step is performed as part of the full uninstallation of a module.
        """ 

        ids = self.search(cr, uid, [('module', 'in', modules_to_remove)])

        if uid != 1 and not self.pool.get('ir.model.access').check_groups(cr, uid, "base.group_system"):
            raise except_orm(_('Permission Denied'), (_('Administrator access is required to uninstall a module')))

        context = dict(context or {})
        context[MODULE_UNINSTALL_FLAG] = True # enable model/field deletion

        ids_set = set(ids)
        wkf_todo = []
        to_unlink = []
        ids.sort()
        ids.reverse()
        for data in self.browse(cr, uid, ids, context):
            model = data.model
            res_id = data.res_id

            pair_to_unlink = (model, res_id)
            if pair_to_unlink not in to_unlink:
                to_unlink.append(pair_to_unlink)

            if model == 'workflow.activity':
                # Special treatment for workflow activities: temporarily revert their
                # incoming transition and trigger an update to force all workflow items
                # to move out before deleting them
                cr.execute('select res_type,res_id from wkf_instance where id IN (select inst_id from wkf_workitem where act_id=%s)', (res_id,))
                wkf_todo.extend(cr.fetchall())
                cr.execute("update wkf_transition set condition='True', group_id=NULL, signal=NULL,act_to=act_from,act_from=%s where act_to=%s", (res_id,res_id))

        wf_service = netsvc.LocalService("workflow")
        for model,res_id in wkf_todo:
            try:
                wf_service.trg_write(uid, model, res_id, cr)
            except Exception:
                _logger.info('Unable to force processing of workflow for item %s@%s in order to leave activity to be deleted', res_id, model, exc_info=True)

        def unlink_if_refcount(to_unlink):
            for model, res_id in to_unlink:
                external_ids = self.search(cr, uid, [('model', '=', model),('res_id', '=', res_id)])
                if set(external_ids)-ids_set:
                    # if other modules have defined this record, we must not delete it
                    continue
                _logger.info('Deleting %s@%s', res_id, model)
                try:
                    cr.execute('SAVEPOINT record_unlink_save')
                    self.pool.get(model).unlink(cr, uid, [res_id], context=context)
                except Exception:
                    _logger.info('Unable to delete %s@%s', res_id, model, exc_info=True)
                    cr.execute('ROLLBACK TO SAVEPOINT record_unlink_save')
                else:
                    cr.execute('RELEASE SAVEPOINT record_unlink_save')

        # Remove non-model records first, then model fields, and finish with models
        unlink_if_refcount((model, res_id) for model, res_id in to_unlink
                                if model not in ('ir.model','ir.model.fields'))
#        unlink_if_refcount((model, res_id) for model, res_id in to_unlink
#                                if model == 'ir.model.fields')

        ir_model_relation = self.pool.get('ir.model.relation')
        ir_module_module = self.pool.get('ir.module.module')
        modules_to_remove_ids = ir_module_module.search(cr, uid, [('name', 'in', modules_to_remove)])
        relation_ids = ir_model_relation.search(cr, uid, [('module', 'in', modules_to_remove_ids)])
        ir_model_relation._module_data_uninstall(cr, uid, relation_ids, context)

#        unlink_if_refcount((model, res_id) for model, res_id in to_unlink
#                                if model == 'ir.model')

        cr.commit()

        self.unlink(cr, uid, ids, context)
ir_model_data_ext()