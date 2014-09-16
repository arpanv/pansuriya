from openerp.osv import osv,fields

class product_ept(osv.osv):
    _inherit = 'product.product'
    
    def _get_current_amount(self, cr, uid, ids, Name=None, args=None, context=None):
        res = {}
        for product in self.browse(cr, uid, ids):
            res[product.id] = 0.0
            if not product.stone_bid_ids:
                res[product.id] = product.discount
            else:
                stone_bid_ids = self.pool.get('stone.bid.ept').search(cr, uid, [('product_id','=',product.id)],order='id desc')
                if stone_bid_ids:
                    bid_obj = self.pool.get('stone.bid.ept').browse(cr, uid, stone_bid_ids[0])
                    res[product.id] = bid_obj.bid_amount or 0.0
        return res
     
    _columns = {
            'stone_bid_ids' : fields.one2many('stone.bid.ept','product_id','Bid Ids'),
            'current_bid_amount' : fields.function(_get_current_amount, type='float', string='Latest Bid Amount'),       
                }
    
    _defaults = {
                'current_bid_amount':0.0,
                }