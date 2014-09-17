from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import openerp.addons.decimal_precision as dp
from openerp import netsvc

class account_invoice_line(osv.osv):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'
    
    def product_id_change(self, cr, uid, ids, product, uom_id, qty=0, name='', type='out_invoice', partner_id=False, fposition_id=False, price_unit=False, currency_id=False, context=None, company_id=None):
        
        res_final = super(account_invoice_line,self).product_id_change(cr,uid,ids,product,uom_id,qty=qty,type=type,partner_id=partner_id,fposition_id=fposition_id,price_unit=price_unit,currency_id=currency_id,context=context,company_id=company_id)
        res = self.pool.get('product.product').browse(cr, uid, product, context=context)
        
        if not partner_id:
            raise osv.except_osv(_('No Partner Defined !'),_("You must first select a partner !") )
        result = res_final.get('value',False)
        part = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
        result.update({
                        'discount':res.discount,
                        'weight':res.weight,
                        'color_id':res.color_id and res.color_id.id or False,
                        'clarity_id':res.clarity_id and res.clarity_id.id or False,
                        'cut_id':res.cut_id and res.cut_id.id or False,
                        'polish_id':res.polish_id and res.polish_id.id or False,
                        'symmetry_id':res.symmetry_id and res.symmetry_id.id or False,
                        'fluorescence_intensity_id':res.fluorescence_intensity_id and res.fluorescence_intensity_id.id or False,
                        'rapnet_price':res.rapnet_price or 0.00,
                        'price_caret':res.price_caret or 0.00,
                        'certificate_no' : res.certificate_no or '',
                        'shape_id' : res.shape_id and res.shape_id.id or False,
                        })
        #Code Added By Jay
        warning={}
        currency_obj=self.pool.get('res.currency')
        obj_price_type=self.pool.get('product.price.type')
        price=0
        if type in ('in_invoice', 'in_refund'):
#            result.update( {'price_unit': price_unit or res.standard_price,'invoice_line_tax_id': tax_id} )
            #Code Added by jay
            purchase_pricelist_id=part.property_product_pricelist_purchase.id
            price,warning=self._invoice_price_get(cr,uid,purchase_pricelist_id,product,qty,partner_id,uom_id,currency_obj,obj_price_type,res,price_unit,currency_id,price=price,field="list_price")
        #result.update( {'price_unit': price_unit or res.standard_price,'invoice_line_tax_id': tax_id} )
            #ADDED END
        else:            
#            result.update({'price_unit': res.list_price, 'invoice_line_tax_id': tax_id})
            #Code Added by jay
            sale_pricelist_id=part.property_product_pricelist.id
            price,warning=self._invoice_price_get(cr,uid,sale_pricelist_id,product,qty,partner_id,uom_id,currency_obj,obj_price_type,res,price_unit,currency_id,price=price,field="standard_price")
            if res and part.property_product_pricelist.currency_id.id != currency_id:
                rapnet_price = currency_obj.compute(cr, uid, part.property_product_pricelist.currency_id.id,currency_id,  res.rapnet_price, round=False)
                price_caret = currency_obj.compute(cr, uid, part.property_product_pricelist.currency_id.id,currency_id,  res.price_caret, round=False)
                result.update( {'rapnet_price': rapnet_price,'price_caret':price_caret} )
                
        result.update( {'price_unit': price} )
        res_final['value'].update(result)
        return res_final
    
    def _invoice_price_get(self,cr,uid,pricelist_id,product,qty,partner_id,uom,currency_obj,obj_price_type,res,price_unit,currency_id,price=0,field="standard_price",warning={}):
        if pricelist_id:
            price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist_id],
                                                                 product, qty or 1.0, partner_id, {'uom': uom,'date': time.strftime('%Y-%m-%d'),})[pricelist_id]
            if price is False:
                warning = {
                           'title': 'No valid pricelist line found !',
                           'message':
                           "Couldn't find a pricelist line matching this product and quantity.\n"
                           "You have to change either the product, the quantity or the pricelist."
                           }
            else:
                currency_pricelist=self.pool.get('product.pricelist').browse(cr,uid,pricelist_id)
                if currency_pricelist.currency_id.id != currency_id:
                    price=currency_obj.compute(cr,uid,currency_pricelist.currency_id.id,currency_id,price,round=True,context={})
        else:
            obj_price_id=obj_price_type.search(cr,uid,[('field','=',field)])
            obj_price_currency=obj_price_type.browse(cr,uid, obj_price_id[0])
            price=price_unit or eval("res."+field)
            if obj_price_currency.currency_id.id != currency_id:
                price = currency_obj.compute(cr,uid,obj_price_currency.currency_id.id,currency_id,price,round=True,context={})
            if uom:
                uom = self.pool.get('product.uom').browse(cr, uid, uom)
                if res.uom_id.category_id.id == uom.category_id.id:
                    price = price * uom.factor_inv
        return price,warning

    def _amount_line(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        res = {}
    
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        for line in self.browse(cr, uid, ids):
            ppc = 0.0
            price=0.0
            res[line.id] = {
                'price_subtotal': 0.0,
                'price_caret': 0.0,
            }
            if line.product_id.is_certified and not line.product_id.is_fancy_color:            
                ppc = line.rapnet_price * (1 + (line.discount/100))
                price = ppc * line.weight * line.quantity
            else:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0) * line.quantity
            taxes = tax_obj.compute_all(cr, uid, line.invoice_line_tax_id, price, line.quantity, product=line.product_id, partner=line.invoice_id.partner_id)
            res[line.id]['price_subtotal']= taxes['total']
            res[line.id]['price_caret']=ppc
            if line.invoice_id :
                cur = line.invoice_id.currency_id
                res[line.id]['price_subtotal']=cur_obj.round(cr, uid, cur, taxes['total'])
                res[line.id]['price_caret']=cur_obj.round(cr, uid, cur, ppc)
        return res
    
    _columns = {
                    'price_subtotal': fields.function(_amount_line, string='Amount', multi='true',type="float",
                     digits_compute= dp.get_precision('Account'), store=True),  
                    'price_caret' : fields.function(_amount_line, string='PPC', multi='true', digits_compute= dp.get_precision('Account')),                              
                    'lot_id':fields.many2one('stock.production.lot'),
                    'certificate_no' : fields.char('CERTIFICATE#'),
                    'shape_id' : fields.many2one('product.shape', 'Shape'),
                    'price_unit': fields.float('PRICE', required=True, digits_compute= dp.get_precision('Account')),
                    'discount': fields.float('BACK (%)', digits_compute= dp.get_precision('Discount')),                    
                    'weight':fields.float(string='CRT'),
                    'lot_weight':fields.float(string='Weight'),                    
                    'color_id' : fields.many2one('product.color',string='CLR'),
                    'clarity_id' : fields.many2one('product.clarity', string="Clarity"),
                    'cut_id' : fields.many2one('product.cut', string="Cut"),
                    'polish_id' : fields.many2one('product.polish', string="Polish"),
                    'symmetry_id' : fields.many2one('product.symmetry', string='Symm'),
                    'fluorescence_intensity_id' : fields.many2one('product.fluorescence.intensity', string='Flu.Inte'),
                    'rapnet_price':fields.float(digits_compute= dp.get_precision('Product Price'),string='RAPNET'),
                    #'price_caret':fields.float(digits_compute= dp.get_precision('Product Price'),string='PPC',help='Price/Carat'),
                }
account_invoice_line()
class account_invoice(osv.osv):
    _name='account.invoice'
    _inherit = 'account.invoice'
       
#     def _avg_discount(self,cr,uid,ids,field_name, arg,context=None):        
#         res = {}
#         for invoice in self.browse(cr, uid, ids, context=context):
#             res[invoice.id] = 0.0
#             
#             total_amount = 0.00
#             total_repnet_amount = 0.00
#             
#             if invoice.invoice_line:
#                 for line in invoice.invoice_line:
#                     total_amount += line.price_subtotal
#                     total_repnet_amount+=line.price_unit*line.quantity
#                                  
#                 res[invoice.id] = (total_amount / total_repnet_amount * 100) - 100            
#         return res
    def _avg_discount(self,cr,uid,ids,field_name, arg,context=None):        
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = 0.00
            
            total_amount = 0.00
            total_repnet_amount = 0.00
            if invoice.invoice_line:
                for line in invoice.invoice_line:
                    if line.product_id.is_certified:
                        total_amount += line.price_subtotal
                        total_repnet_amount+= line.rapnet_price * line.weight * 1
                
                if total_repnet_amount != 0:
                    res[invoice.id] = (total_amount / total_repnet_amount * 100) - 100                              
        return res  
    
    def _get_invoice_line(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('account.invoice.line').browse(cr, uid, ids, context=context):
            result[line.invoice_id.id] = True
        return result.keys()
    _columns = {
                    'avg_discount': fields.function(_avg_discount, digits_compute=dp.get_precision('Account'), string='Avg. Discount',
                                    store={
                                           'account.invoice': (lambda self, cr, uid, ids, c={}: ids, [], 20),                                           
                                           'account.invoice.line': (_get_invoice_line, ['discount','invoice_id'], 20),
            },
            ),
                }
account_invoice()