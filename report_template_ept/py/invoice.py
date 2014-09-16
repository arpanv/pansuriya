from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import openerp.addons.decimal_precision as dp
from openerp import netsvc

class account_invoice(osv.osv):
    _name='account.invoice'
    _inherit = 'account.invoice'
    
    _columns = {
                'shop_id': fields.many2one('sale.shop', 'Shop', readonly=True, states={'draft': [('readonly', False)]}),
                }
    
    def invoice_print(self, cr, uid, ids, context=None):
        '''
        This function prints the invoice and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        self.write(cr, uid, ids, {'sent': True}, context=context)
        datas = {
             'ids': ids,
             'model': 'account.invoice',
             'form': self.read(cr, uid, ids[0], context=context)
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account.invoice.ept',
            'datas': datas,
            'nodestroy' : True
        }
        
account_invoice()