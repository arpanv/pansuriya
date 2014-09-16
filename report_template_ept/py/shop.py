from openerp.osv import fields, osv

class sale_shop(osv.osv):
    _name = 'sale.shop'
    _inherit='sale.shop'
    
    _columns = {
                    'partner_id':fields.many2one('res.partner',string='Address')
                }
sale_shop()
