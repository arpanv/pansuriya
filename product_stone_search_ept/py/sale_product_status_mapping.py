from openerp.osv import fields, osv
from openerp import pooler
class sale_product_status_mapping(osv.osv):
    _name = 'sale.product.status.mapping'
    _description = 'Product Status Mapping to Sale Order Status'
    
    _columns = {
                    'sale_state':fields.selection([
                       ('draft', 'Draft Quotation'),                                                                     
                       ('cancel', 'Cancelled'),                       
                       ('progress', 'Sales Order'),
                       ('manual', 'Sale to Invoice'),
                       ('shipping_except', 'Shipping Exception'),
                       ('invoice_except', 'Invoice Exception'),
                       ('done', 'Done'),
                       ], 'Order Status',),
                    'product_status_id':fields.many2one('product.status','Product Status')
                }