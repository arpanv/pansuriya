from openerp.osv import osv,fields
import magento
class procduct(osv.osv):
    _name = 'product.test'
    _rec_name = 'pnm'
    _columns = {
                'pnm' : fields.char('Name', size=256),
                'price' : fields.integer('Price', size=256),
                }
    def create(self, cr, uid, vals, context):
        new_id = super(procduct, self).create(cr, uid, vals)
        #req_pro = self.pool.get('stock.picking').issued_return_info(cr, uid, [494])
        #self.pool.get('stock.picking').move_info(cr, uid, 28)
        #self.pool.get('stock.picking').do_partial_ept(cr, uid, 526,[895,896,897],[])
        self.pool.get('stock.picking').return_stone_info(cr, uid,[897])
        return new_id
    
#     def test_report(self, cr, uid, ids, context):
#         return {'type': 'ir.actions.report.xml', 'report_name': 'test.report', 'nodestroy': True}
#         return True

'''
########################code for enter record in magento_website_product
           
        website_obj = self.pool.get('magento.instance.website')
        website_product_obj = self.pool.get('magento.website.product')
        product_obj = self.pool.get('product.product')
        website_ids = website_obj.search(cr, uid, [], context={})
        website = website_obj.browse(cr, uid, website_ids[0], context=context)
        instance = website.instance
        with magento.Product(
            instance.url, instance.api_user, instance.api_key
        ) as product_api:
            all_product_ids = product_api.list()
            for data in all_product_ids:
                pid = product_obj.search(cr, uid, [('default_code','=',data.get('sku'))], context={})
                if pid:
                    website_product_obj.create(cr, uid, {
                        'magento_id': data.get('product_id'),
                        'website': website_ids[0],
                        'product': pid[0],
                    }, context=context)
                    
########################
'''