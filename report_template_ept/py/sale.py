from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import openerp.addons.decimal_precision as dp
from openerp import netsvc
class sale_order(osv.osv):
    _name = 'sale.order'
    _inherit = 'sale.order'
    
    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        invoice_vals = {}
        invoice_vals = super(sale_order,self)._prepare_invoice(cr,uid,order,lines,context=context)
        invoice_vals['shop_id'] = order.shop_id.id
        return invoice_vals
    
    
    def print_quotation(self, cr, uid, ids, context=None):
        '''
        This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(uid, 'sale.order', ids[0], 'quotation_sent', cr)
        datas = {
                 'model': 'sale.order',
                 'ids': ids,
                 'form': self.read(cr, uid, ids[0], context=context),
        }
        return {'type': 'ir.actions.report.xml', 'report_name': 'sale.order.ept', 'datas': datas, 'nodestroy': True}
sale_order()