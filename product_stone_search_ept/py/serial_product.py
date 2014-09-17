import math
import re
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class stock_location(osv.osv):
    _name = 'stock.location'
    _inherit = 'stock.location'
    
    def _complete_name(self, cr, uid, ids, name, args, context=None):
        """ Forms complete name of location from parent location to child location.
        @return: Dictionary of values
        """
        res = {}
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


class serial_product_ept(osv.osv):
    _inherit = 'stock.production.lot'
    
    def _get_product(self, cr, uid, ids, context=None):
        lot_ids = self.pool.get('stock.production.lot').search(cr,uid,[('categ_id','in',ids)],context=context)
        return lot_ids
    
    def _get_lot_ids(self, cr, uid, ids, context=None):
        result = {}
        for move_line in self.pool.get('stock.move').browse(cr, uid, ids, context=context):
            if move_line.state == 'done' and move_line.prodlot_id:
                result[move_line.prodlot_id.id] = True
        return result.keys()
    
    def _get_product_category(self,cr,uid,ids,context=None):
        lot_ids = self.pool.get('stock.production.lot').search(cr,uid,[('product_id','in',ids)],context=context)
        return lot_ids
    
    def _get_different_price(self,cr,uid,ids,field_name,arg,context=None):
        res = {}
        for obj in self.browse(cr,uid,ids,context=context):
            res[obj.id] = {'rapnet_price': 0.0,'price_caret': 0.0,'total_price': 0.0}
            rapnet_price = 0.0
            price_caret = 0.0
            list_price = 0.0
            if obj.categ_id.sale_price:
                config_ids = self.pool.get('ir.config_parameter').search(cr,uid,[('key','=','product_rapnet_price_multiple')]);
                if config_ids:
                    parameter_obj=self.pool.get('ir.config_parameter').browse(cr,uid,config_ids[0])
                    if obj.categ_id.sale_price:
                        rapnet_price = obj.categ_id.sale_price * float(parameter_obj.value)
                else:                                                 
                    rapnet_price = obj.categ_id.sale_price
                
            if obj.discount > 0.0:
                price_caret = rapnet_price - (rapnet_price * (obj.discount/100))
                list_price = price_caret * obj.weight
            res[obj.id]['rapnet_price'] = rapnet_price
            res[obj.id]['price_caret'] = price_caret
            res[obj.id]['list_price'] = list_price
            res[obj.id]['unit_price'] = rapnet_price * obj.weight
        return res
    
    def _get_latest_location(self,cr,uid,ids,field_name, arg, context=None):
        res = {}
        move_pool = self.pool.get('stock.move')
        for obj in self.browse(cr,uid,ids,context=context):
            res[obj.id] = False
            if obj.move_ids :
                move_search_ids = move_pool.search(cr,uid,[('prodlot_id','=',obj.id),('state','=','done')],order='id desc',limit=1)
                if move_search_ids:
                    move_id = move_pool.browse(cr,uid,move_search_ids[0],context=context)
                    if move_id :
                        res[obj.id] = move_id.location_dest_id.id
        return res
        
    def get_stones(self,cr,uid,args=None):
        if args:
            stone_ids = self.search(cr, uid, args)
            return self.browse(cr,uid,stone_ids)
        
            
        else:
            return False
            
    _columns = {
                'certificate_no' : fields.char('CERTIFICATE#'),
                'shape_id' : fields.many2one('product.shape', 'Shape'),
                'weight' : fields.float('Weight'),
                'color_id' : fields.many2one('product.color', "Color"),
                'clarity_id' : fields.many2one('product.clarity', "Clarity"),
                'cut_id' : fields.many2one('product.cut', "Cut"),
                'polish_id' : fields.many2one('product.polish', "Polish"),
                'symmetry_id' : fields.many2one('product.symmetry', 'Symmetry'),
                'fluorescence_intensity_id' : fields.many2one('product.fluorescence.intensity', 'Fluorescence Intensity'),
                'product_length' : fields.float('Length'),
                'product_width' : fields.float('Width'),
                'product_height' : fields.float('Height'),
                'milky' : fields.char('Milky', size=128),
                'shade' : fields.char('Shade', size=128),
                'lab_id': fields.many2one('product.lab', 'Lab'),
                'laser_inspection' : fields.boolean('Laser Inscription'),
#                'shipped_id' : fields.many2one('product.shipped', 'Shipped By'),
                'tinge' : fields.char('Tinge', size=128),
                'rfid_tag' : fields.char('RFID Tag', size=128),
                'product_table' : fields.float('Table %'),
                'gridle_thin_id' : fields.many2one('product.gridle_thin', 'Girdle Thin'),
                'gridle_thick_id' : fields.many2one('product.gridle_thick', 'Girdle Thick'),

#added
                'gridle_percentage' : fields.float('Gridle %'),
                'gridle_id' : fields.many2one('product.gridle','Gridle'),
                
                'gridle_condition' : fields.char('Gridle Condition'),
                'culet_id' : fields.many2one('product.culet', 'Culet Size'),
                'culet_condition' : fields.char('Culet Condition'),
                'fluorescence_color_id' : fields.many2one('product.fluorescence.color', 'Fluorescence Color'),
                'crown_height' : fields.float('Crown Height'),
                'crown_angle' : fields.float('Crown Angle'),
                'pavilion_depth' : fields.float('Pavilion Depth'),
                'pavilion_height' : fields.float('Pavilion Angle'),
                'fancy_color_id' : fields.many2one('product.fancy.color', 'Fancy Color'),
                'fancy_color_intensity' : fields.float('Fancy Color Intensity'),
                'fancy_color_overtone' : fields.char('Fancy Color Overtone', size=128),
                'rough_origin' : fields.char('Rough Origin', size=256),
                'product_depth' : fields.float('Depth'),
                'insure_id' : fields.many2one('product.insure', 'Insured By'),
                'status_id' : fields.many2one('product.status', 'Status'),
                'rapnet_price':fields.function(_get_different_price,type='float',multi='sums',digits_compute=dp.get_precision('Product Price'),string="RAPNET",help="This is price which is defined in product's selected category",
                                               store={
                                                    'stock.production.lot': (lambda self, cr, uid, ids, c={}: ids, ['categ_id'], 10),                                                    
                                                    'product.category': (_get_product, ['sale_price'],10),},
                                               ),
                'discount':fields.float('BACK'),
                'price_caret':fields.function(_get_different_price,type='float',multi='sums',digits_compute=dp.get_precision('Product Price'),string="PPC",help="Price/Caret",
                                              store={
                                                    'stock.production.lot': (lambda self, cr, uid, ids, c={}: ids, ['categ_id','discount'], 10), 
                                                    'product.category': (_get_product, ['sale_price'], 10),},
                                               ),
                'list_price':fields.function(_get_different_price,type='float',multi='sums',digits_compute=dp.get_precision('Product Price'),string="Total Price",help="Price/Caret * Weight",
                                              store={
                                                    'stock.production.lot': (lambda self, cr, uid, ids, c={}: ids, ['categ_id','discount','weight'],10),
                                                    'product.category': (_get_product, ['sale_price'],10),},
                                               ),
                'unit_price':fields.function(_get_different_price,type='float',multi='sums',digits_compute=dp.get_precision('Product Price'),string="PRICE",
                                              store={
                                                    'stock.production.lot': (lambda self, cr, uid, ids, c={}: ids, ['categ_id','discount','weight'],10),
                                                    'product.category': (_get_product, ['sale_price'],10),},
                                               ),
                'categ_id' : fields.many2one('product.category', 'Product Category'),
                'type':fields.selection([('Regular','Regular'),('Stone','Stone')],"Type"),
                'location_id' : fields.function(_get_latest_location,type='many2one',string='Location',relation='stock.location',
                                                store={
                                                       'stock.production.lot': (lambda self, cr, uid, ids, c={}: ids, ['move_ids'],10),
                                                       'stock.move':(_get_lot_ids,['location_dest_id','state','prodlot_id'],10),
                                                       }                                                       
                                                ),    
                }
    
    def _check_lot_ept(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.product_id and obj.product_id.track_production and obj.product_id.track_incoming and obj.product_id.track_outgoing: 
                return True
            else:
                return False
            
    _constraints = [
                    (_check_lot_ept, 'You must need to configure lot settings in Product screen for this Stone.', ['product_id']),
                    ]
    
    def search(self, cr, uid, args, offset=0, limit=None, order=None,context=None, count=False):
        search_name = []
        tuple_search = []
        num=1;
        for i in args:
            if i[0] == 'name':
                search_name = i[2].split()
                if search_name:
                    while num < len(search_name):
                        num = num + 1
                        tuple_search.append('|')  
                    for j in search_name:
 #                       tuple_search.append(('name','ilike',j))
                         tuple_search.append(('name','ilike',j))
            else :
                tuple_search.append(i)      
                      
        return super(serial_product_ept, self).search(cr, uid, args=tuple_search, offset=offset, limit=limit, order=order,
            context=context, count=count)
    
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
    
serial_product_ept()

class product_status(osv.osv):
    _name = 'product.status'
    _columns = {
                'name' : fields.char('Status', size=512),
#                 'product_ids' : fields.one2many('product.product', 'status_id', 'Products'),
                }
product_status()

class product_insure(osv.osv):
    _name = 'product.insure'
    _columns = {
                'name' : fields.char('Insured By', size=512),
#                 'product_ids' : fields.one2many('product.product', 'insure_id', 'Products'),
                }
product_insure()

class product_fancy_color(osv.osv):
    _name = 'product.fancy.color'
    _columns = {
                'name' : fields.char('Fancy Color', size=512),
#                 'product_ids' : fields.one2many('product.product', 'fancy_color_id', 'Products'),
                }
product_fancy_color()

class product_fluorescence_color(osv.osv):
    _name = 'product.fluorescence.color'
    _columns = {
                'name' : fields.char('Fluorescence Color', size=512),
#                 'product_ids' : fields.one2many('product.product', 'fluorescence_color_id', 'Products'),
                }
product_fluorescence_color()

class product_culet(osv.osv):
    _name = 'product.culet'
    _columns = {
                'name' : fields.char('Culet Size', size=512),
#                 'product_ids' : fields.one2many('product.product', 'culet_id', 'Products'),
                }
product_culet()

class product_gridle_thick(osv.osv):
    _name = 'product.gridle_thick'
    _columns = {
                'name' : fields.char('Girdle Thick', size=512),
#                 'product_ids' : fields.one2many('product.product', 'gridle_thick_id', 'Products'),
                }
product_gridle_thick()

class product_gridle_thin(osv.osv):
    _name = 'product.gridle_thin'
    _columns = {
                'name' : fields.char('Girdle Thin', size=512),
#                 'product_ids' : fields.one2many('product.product', 'gridle_thin_id', 'Products'),
                }
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
#                  'product_ids' : fields.one2many('product.product', 'lab_id', 'Products'),
                }
product_lab()

class product_fluorescence_intensity(osv.osv):
    _name = 'product.fluorescence.intensity'
    _columns = {
                'name' : fields.char('Fluorescence Intensity', size=512),
#                 'product_ids' : fields.one2many('product.product', 'fluorescence_intensity_id', 'Products'),
                }
product_fluorescence_intensity()

class product_symmetry(osv.osv):
    _name = 'product.symmetry'
    _columns = {
                'name' : fields.char('Symmetry', size=512),
#                  'product_ids' : fields.one2many('product.product', 'symmetry_id', 'Products'),
                }
product_symmetry()

class product_polish(osv.osv):
    _name = 'product.polish'
    _columns = {
                'name' : fields.char('Cut', size=512),
#                  'product_ids' : fields.one2many('product.product', 'polish_id', 'Products'),
                }
product_polish()

class product_cut(osv.osv):
    _name = 'product.cut'
    _columns = {
                'name' : fields.char('Cut', size=512),
#                  'product_ids' : fields.one2many('product.product', 'cut_id', 'Products'),
                }
product_cut()

class product_clarity(osv.osv):
    _name = 'product.clarity'
    _columns = {
                'name' : fields.char('Clarity', size=512),
#                  'product_ids' : fields.one2many('product.product', 'clarity_id', 'Products'),
                }
product_clarity()

class product_color(osv.osv):
    _name = 'product.color'
    _columns = {
                'name' : fields.char('Color', size=512),
#                  'product_ids' : fields.one2many('product.product', 'color_id', 'Products'),
                }
product_color()

class product_shape(osv.osv):
    _name = 'product.shape'
    _columns = {
                'name' : fields.char('Shape', size=512),
#                 'product_ids' : fields.one2many('product.product', 'shape_id', 'Products'),
                }
product_shape()

######added    
class product_gridle(osv.osv):
    _name = 'product.gridle'
    _columns = {
                'name' : fields.char('Gridle', size=512),
                'code' : fields.char('Code'),
                }
product_gridle()