from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class product_category(osv.osv):
     _inherit='product.category'
     _columns = {
                 'sale_price' : fields.float('Sale Price',digits_compute=dp.get_precision('Product Price')),
                 'shape_id':fields.many2one('product.shape',string="Shape"),
                 'weight_from':fields.float('Weight From'),
                 'weight_to':fields.float('Weight To'),
                 'color_id':fields.many2one('product.color',string='Color'),
                 'clarity_id':fields.many2one('product.clarity',string='Clarity', ondelete='restrict'),
                 'shape_line':fields.one2many('shape.line','categ_id','Shape Lines'),
                }
product_category()
    
class shape_line(osv.osv):
    _name = 'shape.line'
    _columns = {
                'categ_id' : fields.many2one('product.category','Category', ondelete='restrict'),
                'shape_id' : fields.many2one('product.shape',string="Shape", ondelete='restrict'),
                'sale_price' :  fields.float('Sale Price',digits_compute=dp.get_precision('Product Price')),
                }


