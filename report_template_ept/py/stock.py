from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from operator import itemgetter
from itertools import groupby

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import netsvc
from openerp import tools
from openerp.tools import float_compare, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)

class stock_picking(osv.osv):
    _name = "stock.picking"
    _inherit = "stock.picking"
    
    def _prepare_invoice(self, cr, uid, picking, partner, inv_type, journal_id, context=None):
        invoice_vals = {}
        invoice_vals=super(stock_picking,self)._prepare_invoice(cr,uid,picking, partner, inv_type, journal_id,context=context)
        if picking.sale_id :
            invoice_vals['shop_id'] = picking.sale_id.shop_id.id
        return invoice_vals
    
stock_picking()