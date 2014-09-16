from openerp.osv import osv,fields
import magento
class exception_handler(osv.osv):
    _name = 'exception.handler'
    _rec_name = 'exce_id'
    _columns = {
                'exce_id' : fields.integer('Id', size=126),
                'create_date' : fields.datetime('Created Date'),
                'data' : fields.text('Error'),
                'state' : fields.selection([
                                            ('exception','Exception'),
                                            ('done','Done'),
                                            ],'Status'),
                'model_nm' : fields.char('Model', size=256),
                }
    
    def reimport(self, cr, uid, ids, context):
        """
        In this method we can Re-import the sale order from magento, which is in exception state.
        """
        if not context:
            context={}
        sale_obj = self.pool.get('sale.order')
        store_view_ids = self.pool.get('magento.store.store_view').search(cr, uid, [], context=context)
        store_view_obj = self.pool.get('magento.store.store_view').browse(cr, uid, store_view_ids[0], context=context)
        magento_state_obj = self.pool.get('magento.order_state')
        store_view = store_view_obj
        instance = store_view.instance
        
        order_states = magento_state_obj.search(cr, uid, [
            ('instance', '=', instance.id),
            ('use_for_import', '=', True)
        ])
        order_states_to_import_in = [
            state.code for state in magento_state_obj.browse(
                cr, uid, order_states, context=context
            )
        ]
        context.update({
            'magento_instance': instance.id,
            'magento_website': store_view.website.id,
            'magento_store_view': store_view.id,
        })
        
        with magento.Order(
            instance.url, instance.api_user, instance.api_key
        ) as order_api:
            new_sales = []
            mag_order_ids = []
            #sale_order_ids = self.search(cr, uid, [('model_nm','=','sale.order')])
            data = self.read(cr, uid, ids, ['exce_id'], context)
            for item in data:
                mag_order_ids.append(item.get('exce_id'))
            filter = {
                        'store_id': {'=': store_view.magento_id},
                        'state': {'in': order_states_to_import_in},
                        'increment_id': {'in' : mag_order_ids},
                     }
            orders = order_api.list(filter)
            for order in orders:
                reimport_id = self.search(cr, uid, [('exce_id','=',order['increment_id'])], context=context)
                try:
                    new_sales.append(
                    sale_obj.find_or_create_using_magento_data(
                        cr, uid,
                        order_api.info(order['increment_id']), context
                        )
                    )
                    vals = {
                            'exce_id' : order['increment_id'],
                            'state' : 'done',
                            }
                    self.write(cr, uid, reimport_id, vals, context=context)
                except Exception,e:
                    vals = {
                            'data' : e,
                            }
                    self.write(cr, uid, reimport_id, vals, context=context)
        return new_sales
    
    def reexport(self, cr, uid, ids, context):
        pid = self.pool.get('magento.instance.website').export_catalog_to_magento(cr, uid, ids, context)
        return pid 
    
class selected_order_reimport(osv.osv_memory):
    _name = 'selected.order.reimport'
    
    def selected_reimport(self, cr, uid, ids, context={}):
        if context.get('active_ids',False):
            self.pool.get('exception.handler').reimport(cr, uid, context.get('active_ids'), context=context)
        return {'type': 'ir.actions.act_window_close',}
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
