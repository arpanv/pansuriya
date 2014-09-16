from openerp.osv import fields, osv
class res_partner_bank(osv.osv):
    _name = 'res.partner.bank'
    _inherit = 'res.partner.bank'
    
    _columns = {
                    'display_in_report':fields.boolean("Display in Report")
                }
res_partner_bank()