import math
import re
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
class product_box_ept(osv.osv):
    _name = 'product.box.ept'
    _description = 'Product Box'
    
    _columns = {
                    'name':fields.char('Name',required=True),
                    'code':fields.char('Code'),
                    'product_ids':fields.one2many('product.product','box_id_ept',string="Products"),
                }
    
product_box_ept()