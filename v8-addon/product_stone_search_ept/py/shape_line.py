from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class shape_line(osv.osv):
    _name = 'shape.line'
    _columns = {
                'categ_id' : fields.many2one('product.category','Category'),
                'shape_id' : fields.many2one('product.shape',string="Shape"),
                'sale_price' :  fields.float('Sale Price',digits_compute=dp.get_precision('Product Price')),
                }