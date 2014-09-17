import math
import re
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class stock_tally_ept(osv.osv):
    '''
        Inherit for adding default location and quantity in physical inventory form.
    '''
    _inherit = 'stock.inventory'
    _columns = {
                'default_loc_id' : fields.many2one('stock.location','Location'),
                'default_qty' : fields.integer('Quantity'),
                }

#     def def_location_id_change(self, cr, uid, ids, default_loc_id):
#         location_id=default_loc_id
#         return location_id
    
stock_tally_ept()
    
class stock_inventory_line_ept(osv.osv):
    _inherit = 'stock.inventory.line'

    def _default_stock_location(self, cr, uid, context=None):
        '''
            it will set default location for stone.
        '''
        if context:
            if context.get('default_tally_location_ept', False):
                location_id=context.get('default_tally_location_ept')
                return location_id
        return super(stock_inventory_line_ept, self)._default_stock_location(cr, uid, context)
    
    _defaults = {
         'location_id': _default_stock_location,
     }
     
    def on_change_product_id(self, cr, uid, ids, location_id, product, uom=False, to_date=False, amount=0.0):
        '''
            set default amount(product_qty)
        '''
        if not product:
            return {'value': {'product_qty': 0.0, 'product_uom': False, 'prod_lot_id': False}}            
        obj_product = self.pool.get('product.product').browse(cr, uid, product)
        uom = uom or obj_product.uom_id.id
        
        if not amount:
            amount = self.pool.get('stock.location')._product_get(cr, uid, location_id, [product], {'uom': uom, 'to_date': to_date, 'compute_child': False})[product]
        result = {'product_qty': amount, 'product_uom': uom, 'prod_lot_id': False}
        return {'value': result}
    
stock_inventory_line_ept()


class stock_location(osv.osv):
    _name = 'stock.location'
    _inherit = 'stock.location'
    
    def _complete_name(self, cr, uid, ids, name, args, context=None):
        """ Forms complete name of location from parent location to child location.
        @return: Dictionary of values
        """
        res = {}
#####added 
        context=context or {}
        
        for m in self.browse(cr, uid, ids, context=context):
            if context.get('no_complete_name'):
                res[m.id] = m.name
                return res
            names = [m.name]
            parent = m.location_id
            while parent:
                names.append(parent.name)
                parent = parent.location_id
            res[m.id] = ' / '.join(reversed(names))
        return res
    
stock_location()

class product_extand_ept(osv.osv):
    _inherit = 'product.product'

    def get_product_ids(self, cr, uid, location_id, product_ids):
        product_ids = self.search(cr, uid, [('location_id','=',location_id),('id','in',product_ids)])#('write_date','>=',datetime.now()-timedelta(minutes=20))
        return product_ids
    
    def search(self, cr, uid, args, offset=0, limit=None, order=None,context=None, count=False):
        search_name = []
        tuple_search = []
        num=1;
        if context and context.get('stone_import',False):
            return super(product_extand_ept, self).search(cr, uid, args=args, offset=offset, limit=limit, order=order,
            context=context, count=count)
        for i in args:
            if i[0] == 'name':
                search_name = i[2].split()
                if search_name:
                    while num < len(search_name):
                        num = num + 1
                        tuple_search.append('|')  
                    for j in search_name:
                        tuple_search.append(('name','ilike',j))
            else :
                tuple_search.append(i)      
        return super(product_extand_ept, self).search(cr, uid, args=tuple_search, offset=offset, limit=limit, order=order,
            context=context, count=count)
        
    def create(self,cr,uid,vals,context={}):
        product_id = super(product_extand_ept,self).create(cr,uid,vals,context=context)
        shape_id = vals.get('shape_id',False)
        weight = vals.get('weight',0.00)
        color_id = vals.get('color_id',False)
        clarity_id = vals.get('clarity_id',False)
        res=[]
        if shape_id and color_id and clarity_id:
            category_ids = self.pool.get('product.category').search(cr,uid,[('color_id','=',color_id),('weight_from','<=',weight),('weight_to','>=',weight),('clarity_id','=',clarity_id)])
            if not category_ids:
                return product_id
            cr.execute("select id from shape_line where shape_id = %s and categ_id = %s",(shape_id,category_ids[0]))
            result = cr.fetchall()
            if result :
                self.write(cr,uid,[product_id],{'categ_id':category_ids[0]})
                                
        if not vals.get('product_status',False):        
            self.write(cr, uid, [product_id], {'product_status':'available'})
        return product_id
        
            
    def _get_product_ids(self, cr, uid, ids, context=None):
        result = {}
        for move_line in self.pool.get('stock.move').browse(cr, uid, ids, context=context):
            if move_line.state == 'done':
                result[move_line.product_id.id] = True
        return result.keys()
    
    def _get_latest_location(self,cr,uid,ids,field_name, arg, context=None):
        res = {}
        move_pool = self.pool.get('stock.move')
        for obj in self.browse(cr,uid,ids,context=context):
            res[obj.id] = False
            move_search_ids = move_pool.search(cr,uid,[('product_id','=',obj.id),('state','=','done')],order='id desc',limit=1)
            if move_search_ids:
                move_id = move_pool.browse(cr,uid,move_search_ids[0],context=context)
                if move_id :
                    res[obj.id] = move_id.location_dest_id.id
        return res

    def _get_product(self, cr, uid, ids, context=None):
        shape_line_data = self.pool.get('shape.line').read(cr,uid,ids,['categ_id'],context=context)
        categ_ids = [x['categ_id'][0] for x in shape_line_data]
        product_ids = self.pool.get('product.product').search(cr,uid,[('categ_id','in',categ_ids)],context=context)
        return product_ids
    
#     def _get_company_ept(self,cr,uid,ids,context=None):
#         if ids:
#             product = self.browse(cr,uid,ids[0],context=context)
#             if product:
#                 if product.company_id:
#                     return product.company_id
#                 else:
#                     return self.pool.get('res.users').browse(cr,uid,uid).company_id
    
    def _get_different_price(self,cr,uid,ids,field_name, arg, context=None):
        res = {}
        for obj in self.browse(cr,uid,ids,context=context):
            if not obj.is_fancy_color:
                res[obj.id] = {'rapnet_price': 0.0,'price_caret': 0.0,'list_price': 0.0,'price_unit':0.0}
                rapnet_price = 0.0
                price_caret = 0.0
                list_price = 0.0
                
                if not obj.is_certified:
                    res[obj.id]['list_price'] = obj.weight * obj.ppc_non_ceritified
                    return res
                #if context.sale_price:
                config_ids = self.pool.get('ir.config_parameter').search(cr,uid,[('key','=','product_rapnet_price_multiple')]);
                if config_ids:
                    parameter_obj=self.pool.get('ir.config_parameter').browse(cr,uid,config_ids[0])
                    #rapnet_price = obj.categ_id.sale_price * float(parameter_obj.value)
                    
    #########################                
                    if obj.shape_id:
                        cr.execute("select sale_price from shape_line where shape_id = %s and categ_id = %s"%(obj.shape_id.id,obj.categ_id.id))
                        result = cr.fetchall()
                        if result:                            
                            rapnet_price = float(result[0][0]) * float(parameter_obj.value)
                        
                else:                                           
                    rapnet_price = obj.categ_id.sale_price
                    
                if obj.discount:
                    price_caret = rapnet_price + (rapnet_price * (obj.discount/100))
                    list_price = price_caret * obj.weight  
                else :
                    list_price = rapnet_price * obj.weight
                
                    
                res[obj.id]['rapnet_price'] = rapnet_price
                res[obj.id]['price_caret'] = price_caret
                res[obj.id]['list_price'] = list_price
                res[obj.id]['price_unit'] = rapnet_price * obj.weight
            else:
                res[obj.id] = {'list_price': 0.0}
                list_price = obj.price_stone or 0.0
                res[obj.id]['list_price'] = list_price
                res[obj.id]['rapnet_price'] = 0.0
                res[obj.id]['price_caret'] = 0.0
                res[obj.id]['price_unit'] = 0.0
        return res
    
    _columns = {
                'is_fancy_color' : fields.boolean('Is fancy color ?'),
                'price_stone' : fields.float('Price',digits_compute=dp.get_precision('Product Price')),
                'certificate_no' : fields.char('CERTIFICATE#'),
                'shape_id' : fields.many2one('product.shape', 'Shape', ondelete='restrict'),
                'weight' : fields.float('CRT',digits_compute=dp.get_precision('Stock Weight')),
                'color_id' : fields.many2one('product.color', "CLR", ondelete='restrict'),
                'clarity_id' : fields.many2one('product.clarity', "Clarity", ondelete='restrict'),
                'cut_id' : fields.many2one('product.cut', "Cut", ondelete='restrict'),
                'polish_id' : fields.many2one('product.polish', "Polish", ondelete='restrict'),
                'symmetry_id' : fields.many2one('product.symmetry', 'Symmetry', ondelete='restrict'),
                'product_length' : fields.float('Length'),
                'product_width' : fields.float('Width'),
                'product_height' : fields.float('Height'),
                'milky' : fields.char('Milky', size=128),
                'shade' : fields.char('Shade', size=128),
                'lab_id': fields.many2one('product.lab', 'Lab', ondelete='restrict'),
                'laser_inspection' : fields.boolean('Laser Inscription'),
                'tinge' : fields.char('Tinge', size=128),
                'rfid_tag' : fields.char('RFID Tag', size=128),
                'product_table' : fields.float('Table %'),
                'gridle_thin_id' : fields.many2one('product.gridle_thin', 'Girdle Thin', ondelete='restrict'),
                'gridle_thick_id' : fields.many2one('product.gridle_thick', 'Girdle Thick', ondelete='restrict'),

                'gridle_id' : fields.many2one('product.gridle','Gridle', ondelete='restrict'),
                'gridle_percentage' : fields.float('Gridle %'),
                'culet_condition' : fields.many2one('product.culet_condition', 'Culet Condition', ondelete='restrict'),
                'fluorescence_color_id' : fields.many2one('product.fluorescence.color', 'Fluorescence Color', ondelete='restrict'),
                'fluorescence_intensity_id' : fields.many2one('product.fluorescence.intensity', 'Fluorescence Intensity', ondelete='restrict'),
                'diameter' : fields.char('Diameter', size=128),
                'treatment' : fields.char('Treatment', size=128),
                'table_inc' : fields.char('Table Inc.', size=128),
                'eye_clean' : fields.char('Eye clean', size=128),
                'natts' : fields.boolean('Natts'),
                'browness' : fields.boolean('Browness'),
                'hna' : fields.char('HNA', size=128),
                
                'gridle_condition' : fields.char('Gridle Condition', size=128),
                'culet_id' : fields.many2one('product.culet', 'Culet Size', ondelete='restrict'),
                'crown_height' : fields.float('Crown Height'),
                'crown_angle' : fields.float('Crown Angle'),
                'pavilion_depth' : fields.float('Pavilion Depth'),
                'pavilion_height' : fields.float('Pavilion Angle'),
                'fancy_color_id' : fields.many2one('product.fancy.color', 'Fancy Color', ondelete='restrict'),
                'fancy_color_intensity' : fields.many2one('product.fancy.color.intensity' ,'Fancy Color Intensity', ondelete='restrict'),
                'fancy_color_overtone' : fields.many2one('product.fancy.color.overtone', 'Fancy Color Overtone', ondelete='restrict'),
                'rough_origin' : fields.char('Rough Origin', size=256),
                'product_depth' : fields.float('Depth'),
                'insure_id' : fields.many2one('product.insure', 'Insured By', ondelete='restrict'),
                'product_status' : fields.selection([('available','Available'),
                                            ('hold','Hold'),
                                            ('sold','Sold'),
                                            ('on_approval','On Approval'),
                                            ('on_consignment','On Consignment'),
                                            ('offline','Offline'),
                                            ('repair','Repair'),
                                            ('web_sale','Web Sale')], string='Status'),
                
                'cost_price_discount' : fields.float('Cost Price Discount'),
                'rapnet_price':fields.function(_get_different_price,type='float',multi='sums',digits_compute=dp.get_precision('Product Price'),string="RAPNET",help="This is price which is defined in product's selected category",
                                               store={
                                                    'product.product': (lambda self, cr, uid, ids, c={}: ids, ['categ_id','is_certified','ppc_non_ceritified','is_fancy_color'], 10),
                                                    'shape.line': (_get_product, ['sale_price'],10),},
                                               ),
                'discount':fields.float('BACK'),
                'price_caret':fields.function(_get_different_price,type='float',multi='sums',digits_compute=dp.get_precision('Product Price'),string="PPC",help="Price/Caret",
                                              store={
                                                    'product.product': (lambda self, cr, uid, ids, c={}: ids, ['categ_id','discount','is_certified','ppc_non_ceritified','is_fancy_color'], 10), 
                                                    'shape.line': (_get_product, ['sale_price'], 10),},
                                               ),
                'list_price':fields.function(_get_different_price,type='float',multi='sums',digits_compute=dp.get_precision('Product Price'),string="Total Price",help="Price/Caret * Weight",
                                              store={
                                                    'product.product': (lambda self, cr, uid, ids, c={}: ids, ['categ_id','discount','weight','is_certified','ppc_non_ceritified','is_fancy_color'],10),
                                                    'shape.line': (_get_product, ['sale_price'],10),},
                                               ),
                'price_unit':fields.function(_get_different_price,type='float',multi='sums',digits_compute=dp.get_precision('Product Price'),string="PRICE",
                              store={
                                    'product.product': (lambda self, cr, uid, ids, c={}: ids, ['categ_id','discount','weight','is_certified','ppc_non_ceritified','is_fancy_color'],10),
                                    'shape.line': (_get_product, ['sale_price'],10),},
                               ),
                'location_id' : fields.function(_get_latest_location,type='many2one',string='Location',relation='stock.location',
                                store={
                                       'stock.production.lot': (lambda self, cr, uid, ids, c={}: ids, ['move_ids'],10),
                                       'stock.move':(_get_product_ids,['location_dest_id','state','product_id'],10),
                                       }                                                       
                                ),
                'star_length':fields.char('Star Length'),
                'lower_half':fields.char('Lower Half'),                
                'ppc_non_ceritified':fields.float(digits_compute=dp.get_precision('Product Price'),string="Non Certified PPC"),
                'is_certified':fields.boolean('Certified'),
                'is_export':fields.boolean('Exportable'), 
                'box_id_ept':fields.many2one('product.box.ept',string='Box'),
                }
       
    _sql_constraints = [
        ('default_code_unique', 'unique(default_code)', 'Internal Reference must be unique'),
        ('rfid_tag_unique','unique(rfid_tag)','RFID Tag must be unique!!!'),
    ]
    
    def is_certified_checked(self, cr, uid, ids, is_certified):
        '''
            Called from onchange of form view
        '''
        if is_certified:
            return {'value':{'is_export':True}}
        return {'value':{'is_export':False}}
    
    def view_product_by_location(self, cr, uid, ids, context=None):
        data_obj = self.pool.get('ir.model.data')
        data_id = data_obj._get_id(cr, uid, 'stock', 'view_location_tree2')
        view_id = False
        if data_id:
            view_id = data_obj.browse(cr, uid, data_id, context=context).res_id
        form_data_id = data_obj._get_id(cr, uid, 'stock', 'view_location_form')
        if form_data_id:
            form_view_id = data_obj.browse(cr, uid, form_data_id, context=context).res_id
        
        context.update({'product_id': ids[0],'search_default_in_location':1})
        return {
                   'name': _('Stock By Location'),
                   'view_type': 'form',
                   'res_model': 'stock.location',
                   'view_id': False,
                   'context': context,
                   'views': [(view_id, 'tree'), (form_view_id, 'form')],
                   'type': 'ir.actions.act_window',
                   'target': 'new',
                   'nodestroy': True
               }
        return {}
    
#    def create(self, cr, uid, vals, context=None):
#        if vals.get('categ_id'):
#            price = self.pool.get('product.category').read(cr, uid, vals.get('categ_id'), ['sale_price'], context=context)['sale_price'] 
#            vals.update({'rapnet_price' : price})
#        if vals.get('discount'):
#            price_caret = vals['rapnet_price'] - ((vals['rapnet_price']*vals['discount'])/100)
#            vals.update({'price_caret':price_caret})
#            if vals.get('price_caret'):
#                if vals.get('weight'):
#                    total_amount= vals.get('price_caret') * vals.get('weight')
#                    vals.update({'total_price':total_amount})              
#        return super(product_extand_ept, self).create(cr, uid, vals, context=context) 
#      
#    def write(self,cr,uid,ids,vals,context=None):
#        edit_obj=self.browse(cr,uid,ids,context=context)
#        for obj in edit_obj:
#            if obj.categ_id and obj.categ_id.sale_price: 
#                vals.update({'rapnet_price' : obj.categ_id.sale_price})
##            if vals.get('discount'):
##            price_caret = vals['rapnet_price'] - ((vals['rapnet_price']*vals['discount'])/100)
##            vals.update({'price_caret':price_caret})
##            if vals.get('price_caret'):
##                if vals.get('weight'):
##                    total_amount= vals.get('price_caret') * vals.get('weight')
##                    vals.update({'total_price':total_amount})
##                else:
##                    total_amount= vals.get('price_caret') * obj.weight
##                    vals.update({'total_price':total_amount})      
#        return super(product_extand_ept, self).write(cr, uid,ids, vals, context=context)
    
product_extand_ept()

class product_status(osv.osv):
    _name = 'product.status'
    _columns = {
                'name' : fields.char('Status', size=512),
                'code' : fields.char('Code'),
#                 'product_ids' : fields.one2many('product.product', 'status_id', 'Products'),
                }
product_status()

class product_fancy_color_intensity(osv.osv):
    _name = 'product.fancy.color.intensity'
    _columns = {
                'name' : fields.char('Fancy Color Intensity', size=512),
                'code' : fields.char('Code'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product Fancy Color Intensity must be unique'),
    ]
product_fancy_color_intensity()

class product_fancy_color_overtone(osv.osv):
    _name = 'product.fancy.color.overtone'
    _columns = {
                'name' : fields.char('Fancy Color Overtone', size=512),
                'code' : fields.char('Code'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product Fancy Color Overtone must be unique'),
    ]
product_fancy_color_overtone()

class product_insure(osv.osv):
    _name = 'product.insure'
    _columns = {
                'name' : fields.char('Insured By', size=512),
                'code' : fields.char('Code'),
#                 'product_ids' : fields.one2many('product.product', 'insure_id', 'Products'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product insure must be unique'),
    ]
product_insure()

class product_fancy_color(osv.osv):
    _name = 'product.fancy.color'
    _columns = {
                'name' : fields.char('Fancy Color', size=512),
                'code' : fields.char('Code'),
#                 'product_ids' : fields.one2many('product.product', 'fancy_color_id', 'Products'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product fancy color must be unique'),
    ]
product_fancy_color()

class product_fluorescence_color(osv.osv):
    _name = 'product.fluorescence.color'
    _columns = {
                'name' : fields.char('Fluorescence Color', size=512),
                'code' : fields.char('Code'),
#                 'product_ids' : fields.one2many('product.product', 'fluorescence_color_id', 'Products'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product fluorescence color must be unique'),
    ]
product_fluorescence_color()

class product_culet(osv.osv):
    _name = 'product.culet'
    _columns = {
                'name' : fields.char('Culet Size', size=512),
                'code' : fields.char('Code'),
#                 'product_ids' : fields.one2many('product.product', 'culet_id', 'Products'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Name must be unique'),
    ]
product_culet()

class product_gridle_thick(osv.osv):
    _name = 'product.gridle_thick'
    _columns = {
                'name' : fields.char('Girdle Thick', size=512),
                'code' : fields.char('Code'),
                'seq': fields.char('sequence')
#                 'product_ids' : fields.one2many('product.product', 'gridle_thick_id', 'Products'),
                }
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'product Girdle Thick must be unique'),
    ]
product_gridle_thick()

class product_gridle_thin(osv.osv):
    _name = 'product.gridle_thin'
    _columns = {
                'name' : fields.char('Girdle Thin', size=512),
                'code' : fields.char('Code'),
#                 'product_ids' : fields.one2many('product.product', 'gridle_thin_id', 'Products'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'product Girdle Thin must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
    ]
product_gridle_thin()

#class product_shipped(osv.osv):
#    _name = 'product.shipped'
#    _columns = {
#                'name' : fields.char('Shipped By', size=512),
#                'product_ids' : fields.one2many('product.product', 'shipped_id', 'Products'),
#                }
#product_shipped()

class product_lab(osv.osv):
    _name = 'product.lab'
    _columns = {
                'name' : fields.char('Lab', size=512),
                'code' : fields.char('Code'),
#                  'product_ids' : fields.one2many('product.product', 'lab_id', 'Products'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product lab must be unique'),
    ]
product_lab()

class product_fluorescence_intensity(osv.osv):
    _name = 'product.fluorescence.intensity'
    _columns = {
                'name' : fields.char('Fluorescence Intensity', size=512),
                'code' : fields.char('Code'),
                'seq' : fields.char('Sequence')
#                 'product_ids' : fields.one2many('product.product', 'fluorescence_intensity_id', 'Products'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product fluorescence intensity must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
    ]
product_fluorescence_intensity()

class product_symmetry(osv.osv):
    _name = 'product.symmetry'
    _columns = {
                'name' : fields.char('Symmetry', size=512),
                'code' : fields.char('Code'),
                'seq' : fields.char('Sequence')
                }
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product fluorescence intensity must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
    ]
product_symmetry()

class product_polish(osv.osv):
    _name = 'product.polish'
    _columns = {
                'name' : fields.char('Polish', size=512),
                'code' : fields.char('Code'),
                'seq': fields.char('Sequence')
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product polish must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
    ]
product_polish()

class product_cut(osv.osv):
    _name = 'product.cut'
    _columns = {
                'name' : fields.char('Cut', size=512),
                'code' : fields.char('Code'),
                'seq' : fields.char('Sequence')
                }
    def _check_seq(self, cr, uid, ids, context={}):
        for id in self.browse(cr, uid, ids, context=context):
            if int(id.seq) <= 0:
                return False
        return True  
          
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product cut must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK(seq>0)','Sequence must be grater than zero'),
    ]
product_cut()

class product_clarity(osv.osv):
    _name = 'product.clarity'
    _columns = {
                'name' : fields.char('Clarity', size=512),
                'seq' : fields.char('Sequence'),
                'code' : fields.char('Code')
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product clarity must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
    ]
product_clarity()

class product_color(osv.osv):
    _name = 'product.color'
    _columns = {
                'name' : fields.char('Color', size=512),
                'code' : fields.char('Code'),
                'seq' : fields.char('Sequence'),
                }
    
    _sql_constraints = [
         ('name_unique', 'unique(name)', 'Product color must be unique'),
         ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
         ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
         ]
#     _sql_constraints = [
#         ('name_unique', 'unique(name)', 'Product color must be unique'),
#     ]
product_color()

class product_shape(osv.osv):
    _name = 'product.shape'
    _columns = {
                'name' : fields.char('Shape', size=512),
                'code' : fields.char('Code'),
#                 'product_ids' : fields.one2many('product.product', 'shape_id', 'Products'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product shape must be unique'),
    ]
product_shape()
######added    
class product_gridle(osv.osv):
    _name = 'product.gridle'
    _columns = {
                'name' : fields.char('Gridle', size=512),
                'code' : fields.char('Code'),
                'seq' : fields.char('Sequence'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product gridle must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
         ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
    ]
product_gridle()

class product_culet_condition(osv.osv):
    _name = 'product.culet_condition'
    _columns = {
                'name' : fields.char('Culet Condition',size=512),
                'code' : fields.char('code'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product culet condition must be unique'),
    ]
product_culet_condition()
