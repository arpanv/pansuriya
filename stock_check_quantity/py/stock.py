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
class stock_move(osv.osv):
    _name = "stock.move"
    _inherit = "stock.move"          
    def _check_production_lot(self, cr, uid, ids, context=None):        
        for move in self.browse(cr, uid, ids, context=context):
            location_type = move.location_id.usage
            if not move.product_id.allow_multiple_qty:                               
                if move.prodlot_id and move.state == 'done':
                    for m in move.prodlot_id.move_ids:
                        if m.state == 'done' and m.id!=move.id:
                            old_move_location_type = m.location_id.usage
                            if location_type == 'supplier' or location_type == 'production' or location_type == 'inventory' or location_type == 'procurement':
                                if old_move_location_type == 'supplier' or old_move_location_type == 'production' or old_move_location_type == 'inventory' or old_move_location_type == 'procurement':                            
                                    return False
                               
        return True
    
    def _check_quantity(self, cr, uid, ids, context=None):        
        for move in self.browse(cr, uid, ids, context=context):
            if not move.product_id.allow_multiple_qty:
                if move.prodlot_id and move.product_qty>1:
                    return False   
                else:
                    return True
            else:
                return True                                                          
        return True
    
    _constraints = [        
        (_check_production_lot,
            'Please choose proper Production LOT, Lot number already been used.',
            ['prodlot_id']),
        (_check_quantity,
            'Invalid Quantity!!! Quantity more then 1 is not allowed in one production lot number!!!',
            ['prodlot_id'])]
stock_move()