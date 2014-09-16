from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import openerp.addons.decimal_precision as dp
from openerp import netsvc

class sale_order_line(osv.osv):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'
    
    
    
    
    _columns={
                'lot_id':fields.many2one('stock.production.lot',string="Serial Number"),
              }
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False,lot_id=False, context=None):
        context = context or {}      
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty,
            uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)                
        
        if not product:
            return res
        if pricelist:
            price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist],
                    product, qty or 1.0, partner_id,lot_id, {
                        'uom': uom or res.get('product_uom'),
                        'date': date_order,
                        })[pricelist]
            res['value'].update({'price_unit':price or 0.00})
#         if not context.get('lot_id',False):
#             res['value'].update({'lot_id':False})
                        
        return res
sale_order_line()