# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010-Today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from openerp import tools
from openerp.osv import osv, fields

def _reopen(self, res_id, model):
    return {'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': res_id,
            'res_model': self._name,
            'target': 'new',
            # save original model in context, because selecting the list of available
            # templates requires a model in context
            'context': {
                'default_model': model,
            },
    }

class mail_compose_message(osv.TransientModel):
    _inherit = 'mail.compose.message'

    def _get_templates(self, cr, uid, context=None):
        if context is None:
            context = {}
        model = False
        email_template_obj = self.pool.get('email.template')
        message_id = context.get('default_parent_id', context.get('message_id', context.get('active_id')))

        if context.get('default_composition_mode') == 'reply' and message_id:
            message_data = self.pool.get('mail.message').browse(cr, uid, message_id, context=context)
            if message_data:
                model = message_data.model
        else:
            model = context.get('default_model', context.get('active_model'))
            if not model:
                model = 'mail.compose.message'

        record_ids = email_template_obj.search(cr, uid, [('model', '=', model)], context=context)
        return email_template_obj.name_get(cr, uid, record_ids, context) + [(False, '')]

    _columns = {
        # incredible hack of the day: size=-1 means we want an int db column instead of an str one
        'template_id': fields.selection(_get_templates, 'Template', size=-1),
    }
    
    def save_as_template(self, cr, uid, ids, context=None):
        """ hit save as template button: current form value will be a new
            template attached to the current document. """
        email_template = self.pool.get('email.template')
        ir_model_pool = self.pool.get('ir.model')
        for record in self.browse(cr, uid, ids, context=context):
            model_ids = ir_model_pool.search(cr, uid, [('model', '=', record.model)], context=context)
            model_id = model_ids and model_ids[0] or False
            model_name = ''
            if model_id:
                model_name = ir_model_pool.browse(cr, uid, model_id, context=context).name
            template_name = "%s: %s" % (model_name, tools.ustr(record.subject))
            values = {
                'name': template_name,
                'subject': record.subject or False,
                'body_html': record.body or False,
                'model_id': model_id and model_id[0] or False,
                'attachment_ids': [(6, 0, [att.id for att in record.attachment_ids])]
            }
            
            if not model_id:
                model_id = self.pool.get('ir.model').search(cr, 1, [('model', '=', 'mail.compose.message')])
                values.update({
                               'model_id': model_id and model_id[0] or False,
                               'model' : 'mail.compose.message'
                               })
            template_id = email_template.create(cr, uid, values, context=context)
            record.write(record.onchange_template_id(template_id, record.composition_mode, record.model, record.res_id)['value'])
            return _reopen(self, record.id, record.model)

    