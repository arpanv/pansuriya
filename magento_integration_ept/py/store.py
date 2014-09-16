import logging
import xmlrpclib
from copy import deepcopy
import time

from openerp.osv import fields, osv
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import magento

from magento_integration.api import OrderConfig

_logger = logging.getLogger(__name__)
class WebsiteStoreView(osv.Model):
    """Magento Website Store View
    A store needs one or more store views to be browse-able in the front-end.
    It allows for multiple presentations of a store. Most implementations
    use store views for different languages.
    """
    _name = 'magento.store.store_view'
    _inherit = 'magento.store.store_view'

    _description = 'Magento Website Store View'
    _columns = dict(        
        fiscal_position = fields.many2one('account.fiscal.position',string="Fiscal Position"),
       
    )
    
#####for scheduler    
    
    def import_sale_order_from_magento(self, cr, uid, ids=None, context=None):
        print "\nImporting sale from magento...\n"
        
        if context is None:
            context = {}
        data = self.import_orders(cr, uid, ids, context)
        return data
    
    def export_sale_order_state_to_magento(self, cr, uid, ids=None, context=None):
        print "\nExporting sale state to magento...\n"
        
        if context is None:
            context = {}
        
        data = self.export_orders(cr, uid, ids,context)
        return data
    
    def export_shipped_state_to_magento(self, cr, uid, ids=None, context=None):
        print "\nExporting shipping sale state to magento...\n"
        
        if context is None:
            context = {}
        mag_ins_ids = self.pool.get('magento.instance').search(cr, uid, [])
        for mag_ins_id in mag_ins_ids:
            context.update({'magento_instance': mag_ins_id})
            data = self.export_shipment_status(cr, uid, ids,context)
            
######Overriding for handling run time exception
   
    def import_orders_from_store_view(self, cursor, user, store_view, context):
        """
        Imports orders from store view

        :param cursor: Database cursor
        :param user: ID of current user
        :param store_view: browse record of store_view
        :param context: dictionary of application context data
        :return: list of sale ids
        """
        sale_obj = self.pool.get('sale.order')
        magento_state_obj = self.pool.get('magento.order_state')

        instance = store_view.instance
        new_context = deepcopy(context)
        new_context.update({
            'magento_instance': instance.id,
            'magento_website': store_view.website.id,
            'magento_store_view': store_view.id,
        })
        new_sales = []

        order_states = magento_state_obj.search(cursor, user, [
            ('instance', '=', instance.id),
            ('use_for_import', '=', True)
        ])
        order_states_to_import_in = [
            state.code for state in magento_state_obj.browse(
                cursor, user, order_states, context=context
            )
        ]

        if not order_states_to_import_in:
            raise osv.except_osv(
                _('Order States Not Found!'),
                _(
                    'No order states found for importing orders! '
                    'Please configure the order states on magento instance'
                )
            )

        with magento.Order(
            instance.url, instance.api_user, instance.api_key
        ) as order_api:
            # Filter orders with date and store_id using list()
            # then get info of each order using info()
            # and call find_or_create_using_magento_data on sale
            filter = {
                   'store_id': {'=': store_view.magento_id},
                   'state': {'in': order_states_to_import_in},
                    }
            
            if store_view.last_order_import_time:
                filter.update({
                    'updated_at': {'gteq': store_view.last_order_import_time},
                })
            self.write(cursor, user, [store_view.id], {
                'last_order_import_time': time.strftime(
                    DEFAULT_SERVER_DATETIME_FORMAT
                )
            }, context=context)
            
            orders = order_api.list(filter)
            for order in orders:
                try:
                    new_sales.append(
                        sale_obj.find_or_create_using_magento_data(
                            cursor, user,
                            order_api.info(order['increment_id']), new_context
                        )
                    )
                except Exception,e:
                    vals = {
                                'exce_id' : order['increment_id'],
                                'data' : e,
                                'state' : 'exception',
                                'model_nm' : 'sale.order',
                            }
                    self.pool.get('exception.handler').create(cursor, user, vals, context=context)
        return new_sales

WebsiteStoreView()
