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
    
    def set_to_hold_btn(self,cr, uid, ids, context={},state='hold'):
        """
            It will set stone in hold state.
        """
        sale_line_obj = self.browse(cr ,uid, ids[0],context={})
        product_ids = [line.product_id and line.product_id.id for line in sale_line_obj.order_line]
        self.pool.get("product.product").write(cr, uid, product_ids, {'product_status':state}, context=context)
        return True
    
    def action_cancel(self, cr, uid, ids, context={}):
        """
            When sale order cancel, set stone state available.
        """
        super(sale_order, self).action_cancel(cr, uid, ids, context)
        self.set_to_hold_btn(cr, uid, ids, context,'available')
        return True
    
    def unlink(self,cr, uid, ids, context={}):
        """
            Change status of stone when sale order is delete.
        """
        pro_ids=[]
        for order_id in self.browse(cr, uid, ids,context):
            for line in order_id.order_line:
                if line.product_id:
                    pro_ids.append(line.product_id.id)
                    
        product_ids = self.pool.get('product.product').browse(cr, uid, pro_ids,context={})
        for id in product_ids:
            if id.product_status in ('hold','on_approval'):
                self.pool.get('product.product').write(cr, uid, id.id, {'product_status':'available'},context={})
        return super(sale_order, self).unlink(cr, uid, ids, context=context)
        
    def _avg_discount(self,cr,uid,ids,field_name, arg,context=None):        
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = 0.00
            
            total_amount = 0.00
            total_repnet_amount = 0.00
            if order.order_line:
                for line in order.order_line:
                    if line.product_id.is_certified:
                        total_amount += line.price_subtotal
                        total_repnet_amount+= line.rapnet_price * line.th_weight * line.product_uom_qty
                
                if total_repnet_amount != 0:
                    res[order.id] = (total_amount / total_repnet_amount * 100) - 100                              
        return res
        
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        
        for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()
    
    _columns = {
                    'avg_discount': fields.function(_avg_discount,digits_compute=dp.get_precision('Account'), string='Avg. Discount',help="Average Discount",
                                    store={
                                           'sale.order': (lambda self, cr, uid, ids, c={}: ids, [], 10),
                                           'sale.order.line': (_get_order, ['discount'], 10)
                                           },
                                                    ),
                }
    
        
sale_order()

class sale_order_line(osv.osv):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = {}
        ppc=0.0
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = {
                'price_subtotal': 0.0,
                'price_caret': 0.0,
            }            
            if line.product_id.is_certified and not line.product_id.is_fancy_color:
                ppc = line.rapnet_price * (1 + (line.discount/100))
                price = ppc * line.th_weight * line.product_uom_qty
            else:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                
            taxes = tax_obj.compute_all(cr, uid, line.tax_id, price, line.product_uom_qty, line.product_id, line.order_id.partner_id)
            cur = line.order_id.pricelist_id.currency_id
            res[line.id]['price_subtotal']=cur_obj.round(cr, uid, cur, taxes['total'])
            res[line.id]['price_caret']=ppc
        return res
	
    _columns={
                'price_subtotal': fields.function(_amount_line, string='Subtotal', multi='true', digits_compute= dp.get_precision('Account')),                
                'price_caret' : fields.function(_amount_line, string='PPC', multi='true', digits_compute= dp.get_precision('Account')),
                'product_status' : fields.selection([('available','Available'),
                                            ('hold','Hold'),
                                            ('sold','Sold'),
                                            ('on_approval','On Approval'),
                                            ('on_consignment','On Consignment'),
                                            ('offline','Offline'),
                                            ('repair','Repair')], string='Status'),
                'lot_id':fields.many2one('stock.production.lot'),
                'certificate_no' : fields.char('CERTIFICATE#'),
                'shape_id' : fields.many2one('product.shape', 'Shape'),
                'discount': fields.float('BACK (%)', digits_compute= dp.get_precision('Discount'), readonly=True, states={'draft': [('readonly', False)]}),
                'lot_weight': fields.float('Weight', readonly=True,digits_compute=dp.get_precision('Stock Weight'),states={'draft': [('readonly', False)]}),
                'th_weight': fields.float('CRT', readonly=True,digits_compute=dp.get_precision('Stock Weight'),states={'draft': [('readonly', False)]}),
                'color_id' : fields.many2one('product.color','CLR',readonly=True, states={'draft': [('readonly', False)]}),
                'clarity_id' : fields.many2one('product.clarity','Clarity',readonly=True, states={'draft': [('readonly', False)]}),
                'cut_id' : fields.many2one('product.cut','Cut',readonly=True, states={'draft': [('readonly', False)]}),
                'polish_id' : fields.many2one('product.polish','Polish',readonly=True, states={'draft': [('readonly', False)]}),
                'symmetry_id' : fields.many2one('product.symmetry','Symm',readonly=True, states={'draft': [('readonly', False)]}),
                'fluorescence_intensity_id' : fields.many2one('product.fluorescence.intensity','Flu.Inte',readonly=True, states={'draft': [('readonly', False)]}),
                'rapnet_price':fields.float('RAPNET',digits_compute= dp.get_precision('Product Price'),readonly=True, states={'draft': [('readonly', False)]}),
                'price_unit': fields.float('PRICE', required=True, digits_compute= dp.get_precision('Product Price'), readonly=True, states={'draft': [('readonly', False)]}),
                'lab_id': fields.many2one('product.lab', 'Lab'),
                'product_table' : fields.float('Table %'),
                'product_depth' : fields.float('Depth'),
                'crown_angle' : fields.float('Crown Angle'),
                'product_length' : fields.float('Length'),
                'product_width' : fields.float('Width'),
                'product_height' : fields.float('Height'),  
              }
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        context = context or {}      
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty,
                                                             uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
                                                             lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, 
                                                             fiscal_position=fiscal_position, flag=flag, context=context)       
                 
        if not product: 
            return res
        product_vals = self.pool.get('product.product').read(cr,uid,product,['product_status','product_length','product_width','product_height','lab_id','product_table','product_depth','crown_angle','shape_id','certificate_no','discount','weight','color_id','clarity_id','cut_id','polish_id','symmetry_id','fluorescence_intensity_id','rapnet_price'],context=context)
        #Code Added by Jay
        shop_id = context.get('shop',False)
        rapnet_price = product_vals['rapnet_price'] or 0.0
        #price_caret = product_vals['price_caret'] or 0.0
        
        if shop_id:
            shop_obj = self.pool.get('sale.shop').browse(cr,uid,shop_id)
            currency_id = shop_obj.company_id.secondary_currency_ept and shop_obj.company_id.secondary_currency_ept.id or False
            
            if pricelist and currency_id:
                price_list_currency_id = self.pool.get('product.pricelist').browse(cr,uid,pricelist,context=context).currency_id.id
                if currency_id != price_list_currency_id:
                    currency_obj = self.pool.get('res.currency')
                    rapnet_price = currency_obj.compute(cr, uid, currency_id,price_list_currency_id,  rapnet_price, round=False)
                    #price_caret = currency_obj.compute(cr, uid, currency_id,price_list_currency_id,  price_caret, round=False)
        #Code Added Over
        res['value'].update({
                             'product_status':product_vals['product_status'] or '',
                             'product_id':product,
                             'product_uom':uom,
                             'lab_id' : product_vals['lab_id'] and product_vals['lab_id'][0] or False,
                             'product_table' : product_vals['product_table'] or 0.0,
                             'product_depth' : product_vals['product_depth'] or 0.0,
                             'crown_angle' : product_vals['crown_angle'] or 0.0,
                             'discount':product_vals['discount'] or 0.0,
                             'color_id' : product_vals['color_id'] and product_vals['color_id'][0] or False,
                             'clarity_id' : product_vals['clarity_id'] and product_vals['clarity_id'][0] or False,
                             'cut_id' : product_vals['cut_id'] and product_vals['cut_id'][0] or False,
                             'polish_id' :product_vals['polish_id'] and product_vals['polish_id'][0] or False,
                             'symmetry_id' : product_vals['symmetry_id'] and product_vals['symmetry_id'][0] or False,
                             'fluorescence_intensity_id' :product_vals['fluorescence_intensity_id'] and product_vals['fluorescence_intensity_id'][0] or False,
                             'rapnet_price':rapnet_price,
                             #'price_caret':price_caret,
                             'certificate_no' : product_vals['certificate_no'] or '',
                             'shape_id' : product_vals['shape_id'] and product_vals['shape_id'][0] or False,
                             'product_length' : product_vals['product_length'] or 0.0,
                             'product_width' : product_vals['product_width'] or 0.0,
                             'product_height' : product_vals['product_height'] or 0.0,
                             })                 
        return res
    
    #Added by Jay to Set Production Lot number in Invoice Line
    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
        res = super(sale_order_line,self)._prepare_order_line_invoice_line(cr,uid,line,account_id=account_id,context=context)
        res.update({'weight': line.th_weight or 0.0,
                    'color_id' : line.color_id and line.color_id.id or False,                 
                    'clarity_id' : line.clarity_id and line.clarity_id.id or False,
                    'cut_id' : line.cut_id and line.cut_id.id or False,
                    'polish_id' :line.polish_id and line.polish_id.id or False,
                    'symmetry_id' : line.symmetry_id and line.symmetry_id.id or False,
                    'fluorescence_intensity_id' : line.fluorescence_intensity_id and line.fluorescence_intensity_id.id or False,
                    'rapnet_price' : line.rapnet_price or 0.0,
                    'price_caret' : line.price_caret or 0.0,
                    'discount' : line.discount or 0.0, 
                    'shape_id' : line.shape_id and line.shape_id.id or False,
                    'certificate_no' : line.certificate_no or '',                       
                    })         
        return res
sale_order_line()
