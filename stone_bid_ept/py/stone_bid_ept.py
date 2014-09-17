from openerp.osv import osv,fields
from datetime import datetime, timedelta,date

import logging
_logger = logging.getLogger(__name__)

class stone_bid_ept(osv.osv):
    _name = 'stone.bid.ept'
    _columns = {
                'partner_id' : fields.many2one('res.partner','Customer'),
                'product_id' : fields.many2one('product.product','Product'),
                'bid_amount' : fields.float('Bid Amount'),
                'bid_time' : fields.datetime('Bid Date and Time'),
                }
    
    _defaults={
               'bid_time':fields.date.context_today,
               }
    