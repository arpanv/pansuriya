from openerp.osv import osv,fields

class partner_ept(osv.osv):
    _inherit = 'res.partner'
    _columns = {
                'stone_bid_ids' : fields.one2many('stone.bid.ept','partner_id','Bid Ids'),
                }