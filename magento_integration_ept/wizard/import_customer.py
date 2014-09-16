# -*- coding: utf-8 -*-
"""
    import_catalog

    Import catalog

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: AGPLv3, see LICENSE for more details.
"""

import magento
from openerp.osv import osv
from openerp.tools.translate import _


class ImportCustomer(osv.TransientModel):
    "Import catalog"
    _name = 'magento.instance.import_customer'
    

    def import_customer(self, cursor, user, ids, context):
        """
        Import the product categories and products

        :param cursor: Database cursor
        :param user: ID of current user
        :param ids: List of ids of records for this model
        :param context: Application context
        """
        Pool = self.pool
        website_obj = Pool.get('magento.instance.website')

        website = website_obj.browse(
            cursor, user, context['active_id'], context
        )
        instance = website.instance

        
        customer_ids = self.import_customers(cursor, user, website, context)

        return self.open_customers(
            cursor, user, ids, customer_ids, context
        )

    

    def import_customers(self, cursor, user, website, context):
        """
        Imports products for current instance

        :param cursor: Database cursor
        :param user: ID of current user
        :param website: Browse record of website
        :param context: Application context
        :return: List of product IDs
        """
        partner_obj = self.pool.get('res.partner')

        instance = website.instance

        with magento.Customer(
            instance.url, instance.api_user, instance.api_key
        ) as customer_api:
            mag_customers = []
            customers = []

            # Products are linked to websites. But the magento api filters
            # the products based on store views. The products available on
            # website are always available on all of its store views.
            # So we get one store view for each website in current instance.
            mag_customers.extend(
                customer_api.list(
                    website.stores[0].store_views[0].magento_id
                )
            )
            context.update({
                'magento_website': website.id,
                'website': website.id,
                'magento_instance':website.instance.id
            })

            for mag_customer in mag_customers:
                partner_exist = partner_obj.find_using_magento_id(cursor, user, mag_customer['customer_id'], context)                                     
    
                if not partner_exist:
                    partner = partner_obj.find_or_create_using_magento_id(
                            cursor, user, mag_customer['customer_id'], context,
                        )
                    customers.append(partner)
                    
                    customer_details = customer_api.info(mag_customer['customer_id'])
                    address_details = customer_details['billing_address']
                    
                    country_obj = self.pool.get('res.country')
                    state_obj = self.pool.get('res.country.state')
                    #print "------------> %s" %(address_details['country_id'])
                    country = country_obj.search_using_magento_code(
                        cursor, user, address_details['country_id'], context
                    )
                    if address_details.get('region',False):
                        state_id = state_obj.find_or_create_using_magento_region(
                            cursor, user, country, address_details['region'], context
                        ).id
                    else:
                        state_id = None
                        
                    self.pool.get('res.partner').write(cursor,user,[partner.id],
                       {
                            'street': address_details.get('street',False),
                            'state_id': state_id,
                            'country_id': country.id,
                            'city': address_details.get('city',False),
                            'zip': address_details.get('postcode',False),
                            'phone': address_details.get('telephone',False),
                            'fax': address_details.get('fax',False),
                            'company_name_ept':address_details.get('company',False)
                        }
                       )   
                                                     
#                 
#                 partner_invoice_address = \
#                 partner_obj.find_or_create_address_as_partner_using_magento_data(
#                     cursor, user, customer_details['billing_address'], partner, context
#                 )
# 
#                 partner_shipping_address = \
#                     partner_obj.find_or_create_address_as_partner_using_magento_data(
#                         cursor, user, customer_details['shipping_address'], partner, context
#                     )
        return map(int, customers)
    
    


    def open_customers(self, cursor, user, ids, customer_ids, context):
        """
        Opens view for products for current instance

        :param cursor: Database cursor
        :param user: ID of current user
        :param ids: List of ids of records for this model
        :param product_ids: List or product IDs
        :param context: Application context
        :return: View for products
        """
        ir_model_data = self.pool.get('ir.model.data')

        tree_res = ir_model_data.get_object_reference(
            cursor, user, 'base', 'view_partner_tree'
        )
        tree_id = tree_res and tree_res[1] or False

        return {
            'name': _('Magento Instance Customers'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'res.partner',
            'views': [(tree_id, 'tree')],
            'context': context,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', customer_ids)]
        }

ImportCustomer()
