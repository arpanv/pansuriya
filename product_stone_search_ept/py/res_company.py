import math
import re
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class res_company(osv.osv):
    _name = 'res.company'
    _inherit = 'res.company'
    
    _columns={
                'secondary_currency_ept':fields.many2one('res.currency',string="Secondary Currency")
              }
res_company()