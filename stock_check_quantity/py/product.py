from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from operator import itemgetter
from itertools import groupby

from osv import fields, osv
from tools.translate import _
import netsvc
import tools
from tools import float_compare
import decimal_precision as dp
import logging

class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'
    
    _columns = {
                    'allow_multiple_qty':fields.boolean('Allow Multiple Qty')
                }
product_product()