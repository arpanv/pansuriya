import xmlrpclib
import logging
import magento
from openerp.osv import fields, osv
from openerp.tools.translate import _
_logger = logging.getLogger(__name__)
class Sale(osv.Model):
    "Sale"
    _inherit = 'sale.order'
    _columns = dict(    
        magento_increment_id=fields.char(
            "Magento Increment ID", readonly=True
        ),
        )
    def set_to_hold_btn(self,cr, uid, ids, context={},state='hold'):
        sale_line_obj = self.browse(cr ,uid, ids[0],context={})
        product_ids = [line.product_id and line.product_id.id for line in sale_line_obj.order_line]
        self.pool.get("product.product").write(cr, uid, product_ids, {'product_status':state}, context=context)
        return True
    

    def action_cancel(self, cr, uid, ids, context={}):
        super(Sale, self).action_cancel(cr, uid, ids, context)
        self.set_to_hold_btn(cr, uid, ids, context,'available')
        return True
            
        #for line in sale_line_obj.order_line
            #self.pool.get("product.product").write(cr, uid, line.product_id.id, {'state':'hold'}, context={})
    def export_order_status_to_magento(self, cursor, user, sale, context):
            """
            Export order status to magento.
    
            :param cursor: Database cursor
            :param user: ID of current user
            :param sale: Browse record of sale
            :param context: Application context
            :return: Browse record of sale
            """
            if not sale.magento_id:
                return sale
    
            instance = sale.magento_instance
            if sale.state == 'cancel':
                increment_id = sale.name.split(instance.order_prefix)[1]
                # This try except is placed because magento might not accept this
                # order status change due to its workflow constraints.
                # TODO: Find a better way to do it
                try:
                    with magento.Order(
                        instance.url, instance.api_user, instance.api_key
                    ) as order_api:
                        order_api.cancel(increment_id)
                except xmlrpclib.Fault, f:
                    if f.faultCode == 103:
                        return sale
            elif sale.invoiced and not sale.magento_increment_id:
                increment_id  = sale.name[
                    len(instance.order_prefix): len(sale.name)
                ]
                try:
                    #Code added by jay
                    with magento.Invoice(
                        instance.url, instance.api_user, instance.api_key
                    ) as invoice_api:
                        if sale.invoiced:
                            order_increment_id = invoice_api.create(
                                order_increment_id=increment_id, items_qty={}
                            )
                            self.pool.get('sale.order').write(
                            cursor, user, sale.id, {
                                'magento_increment_id': order_increment_id,
                            }, context=context
                        )
                except xmlrpclib.Fault, fault:
                    if fault.faultCode == 102:
                        # A shipment already exists for this order, log this
                        # detail and continue
                        _logger.info(
                            'Invoice for sale %s already exists on magento'
                            % sale.name
                        )                    
            # TODO: Add logic for other sale states also
    
            return sale      
        
    def get_item_line_data_using_magento_data(self, cursor, user, order_data, context):
        """Make data for an item line from the magento data.
        This method decides the actions to be taken on different product types

        :param cursor: Database cursor
        :param user: ID of current user
        :param order_data: Order Data from magento
        :param context: Application context
        :return: List of data of order lines in required format
        """
        website_obj = self.pool.get('magento.instance.website')
        product_obj = self.pool.get('product.product')
        bom_obj = self.pool.get('mrp.bom')

        line_data = []
        for item in order_data['items']:
            if not item['parent_item_id']:
                # If its a top level product, create it
                
                product = product_obj.find_or_create_using_magento_id(
                            cursor, user, item['product_id'],
                            context=context
                        )
                #Code Added by Jay
                tax_percentage = item.get('tax_percent',0.00)
                #Get Company from Instance
                acc_tax_id = False
                if context.get('magento_instance',False):
                    company_id = self.pool.get('magento.instance').browse(cursor,user,context.get('magento_instance'),context=context).company.id
                if company_id:
                    acctax_id = self.pool.get('account.tax').search(cursor,user,[('type_tax_use', '=', 'sale'), ('amount', '=', float(tax_percentage)/100),('company_id','=',company_id)])
                else:
                    acctax_id = self.pool.get('account.tax').search(cursor,user,[('type_tax_use', '=', 'sale'), ('amount', '=', float(tax_percentage)/100)])
                if not acctax_id:
                    acctax_id = self.createAccountTax(cursor,user,id,float(tax_percentage)/100, context)
                    tax_id = [(6, 0, [acctax_id])]
                    acctax_id = [acctax_id]
                else:
                    tax_id = [(6, 0, acctax_id)]
                
                if context.get('magento_website',False):
                    store_view_ids = self.pool.get('magento.store.store_view').search(cursor,user,[('store','=',context.get('magento_website'))],context=context)
                    if store_view_ids:
                        fpos = self.pool.get('magento.store.store_view').browse(cursor,user,store_view_ids[0]).fiscal_position
                        acc_browse = self.pool.get('account.tax').browse(cursor,user,acctax_id,context=context)
                        result_tax_id = self.pool.get('account.fiscal.position').map_tax(cursor, user, fpos, acc_browse)
                        tax_id = [(6, 0, result_tax_id)]
                #Code Added by Jay Over
                values = {
                    'name': item['name'],
                    'price_unit': float(item['price']),
                    'product_uom':
                        website_obj.get_default_uom(
                            cursor, user, context
                        ).id,
                    'product_uom_qty': float(item['qty_ordered']),
                    'magento_notes': item['product_options'],
                    'type': product.procure_method,
                    'product_id':product.id,
                    'certificate_no':product.certificate_no or '',
                    'shape_id':product.shape_id and product.shape_id.id or False,                    
                    'th_weight':product.weight,
                    'color_id':product.color_id and product.color_id.id or False,
                    'clarity_id':product.clarity_id and product.clarity_id.id or False,
                    'cut_id':product.cut_id and product.cut_id.id or False,
                    'polish_id':product.polish_id and product.polish_id.id or False,
                    'symmetry_id':product.symmetry_id and product.symmetry_id.id or False,
                    'fluorescence_intensity_id':product.fluorescence_intensity_id and product.fluorescence_intensity_id.id or False,
                    'rapnet_price':product.rapnet_price or 0.00,
                    'price_caret':product.price_caret or 0.00,    
                    'tax_id':tax_id,                                
                }
                line_data.append((0, 0, values))

            # If the product is a child product of a bundle product, do not
            # create a separate line for this.
            if 'bundle_option' in item['product_options'] and \
                    item['parent_item_id']:
                continue

        # Handle bundle products.
        # Find/Create BoMs for bundle products
        # If no bundle products exist in sale, nothing extra will happen
        bom_obj.find_or_create_bom_for_magento_bundle(
            cursor, user, order_data, context
        )

        return line_data
    
    
    def createAccountTax(self, cr, uid, id, value, context={}):
        instance = context.get('magento_instance',False)
        company_id = False
        if instance:
            company_id = self.pool.get('magento.instance').browse(cr,uid,instance,context=context).company.id
            accounttax_obj = self.pool.get('account.tax')
            accounttax_id = accounttax_obj.create(cr,uid,{'name':'Sales Tax(' + str(value*100) + '%)','amount':float(value),'type_tax_use':'sale','company_id':company_id})
            return accounttax_id
        else:
            accounttax_obj = self.pool.get('account.tax')
            accounttax_id = accounttax_obj.create(cr,uid,{'name':'Sales Tax(' + str(value*100) + '%)','amount':float(value),'type_tax_use':'sale'})
            return accounttax_id
    
    def create_using_magento_data(self, cursor, user, order_data, context):
        """
        Create a sale order from magento data

        :param cursor: Database cursor
        :param user: ID of current user
        :param order_data: Order Data from magento
        :param context: Application context
        :returns: Browse record of sale order created
        """
        currency_obj = self.pool.get('res.currency')
        store_view_obj = self.pool.get('magento.store.store_view')
        partner_obj = self.pool.get('res.partner')

        store_view = store_view_obj.browse(
            cursor, user, context['magento_store_view'], context
        )
        if not store_view.shop:
            raise osv.except_osv(
                _('Not Found!'),
                _(
                    'Magento Store %s should have a shop configured.'
                    % store_view.store.name
                )
            )
        if not store_view.shop.pricelist_id:
            raise osv.except_osv(
                _('Not Found!'),
                _(
                    'Shop on store %s does not have a pricelist!'
                    % store_view.store.name
                )
            )

        instance = store_view.instance

        currency = currency_obj.search_using_magento_code(
            cursor, user, order_data['order_currency_code'], context
        )
        if order_data['customer_id']:
            partner = partner_obj.find_or_create_using_magento_id(
                cursor, user, order_data['customer_id'], context
            )
        else:
            partner = partner_obj.create_using_magento_data(
                cursor, user, {
                    'firstname': order_data['customer_firstname'],
                    'lastname': order_data['customer_lastname'],
                    'email': order_data['customer_email'],
                    'magento_id': 0
                },
                context
            )

        partner_invoice_address = \
            partner_obj.find_or_create_address_as_partner_using_magento_data(
                cursor, user, order_data['billing_address'], partner, context
            )

        partner_shipping_address = \
            partner_obj.find_or_create_address_as_partner_using_magento_data(
                cursor, user, order_data['shipping_address'], partner, context
            )

        sale_data = {
            'name': instance.order_prefix + order_data['increment_id'],
            'shop_id': store_view.shop.id,
            'company_id':instance.company.id,
            'date_order': order_data['created_at'].split()[0],
            'partner_id': partner.id,
            'pricelist_id': store_view.shop.pricelist_id.id,
            'currency_id': currency.id,
            'partner_invoice_id': partner_invoice_address.id,
            'partner_shipping_id': partner_shipping_address.id,
            'magento_id': int(order_data['order_id']),
            'magento_instance': instance.id,
            'magento_store_view': store_view.id,
            'fiscal_position':store_view.fiscal_position and store_view.fiscal_position.id or False,  #Added by Jay            
            'order_line': self.get_item_line_data_using_magento_data(
                cursor, user, order_data, context
            )
        }

        if float(order_data.get('shipping_amount')):
            sale_data['order_line'].append(
                self.get_shipping_line_data_using_magento_data(
                    cursor, user, order_data, context
                )
            )

        if float(order_data.get('discount_amount')):
            sale_data['order_line'].append(
                self.get_discount_line_data_using_magento_data(
                    cursor, user, order_data, context
                )
            )

        sale_id = self.create(
            cursor, user, sale_data, context=context
        )

        sale = self.browse(cursor, user, sale_id, context)
        if sale:
            self.set_to_hold_btn(cursor, user, [sale.id], context,'hold')
        # Process sale now
        self.process_sale_using_magento_state(
            cursor, user, sale, order_data['state'], context
        )

        return sale

##################
   
    def process_sale_using_magento_state(
        self, cursor, user, sale, magento_state, context
    ):
                # TODO: Improve this method for invoicing and shipping etc
        magento_order_state_obj = self.pool.get('magento.order_state')

        state_ids = magento_order_state_obj.search(cursor, user, [
            ('code', '=', magento_state),
            ('instance', '=', context['magento_instance'])
        ])

        if not state_ids:
            raise osv.except_osv(
                _('Order state not found!'),
                _('Order state not found/mapped in OpenERP! '
                  'Please import order states on instance'
                 )
            )

        state = magento_order_state_obj.browse(
            cursor, user, state_ids[0], context=context
        )
        openerp_state = state.openerp_state

        # If order is canceled, just cancel it
        if openerp_state == 'cancel':
            self.action_cancel(cursor, user, [sale.id], context)
            return
         
        #if openerp_state == 'sent':
            #return
        
        # Order is not canceled, move it to quotation
        #self.action_button_confirm(cursor, user, [sale.id], context)

        if openerp_state in ['closed', 'complete', 'processing']:
            self.action_wait(cursor, user, [sale.id], context)

        if openerp_state in ['closed', 'complete']:
            self.action_done(cursor, user, [sale.id], context)
            
########################  
   
    def get_shipping_line_data_using_magento_data(self, cr, uid, order_data, context):    
        data = super(Sale, self).get_shipping_line_data_using_magento_data(cr, uid, order_data, context)
        #product_id = self.pool.get('product.product').find_or_create_magento_shipping(cr, uid, order_data['default_code'], context)
        product_id = self.pool.get('product.product').find_or_create_magento_shipping(cr, uid, context)
        
        data[2].update({'product_id':product_id})
        return data
 
Sale()
