import magento
from openerp.osv import osv
from openerp.tools.translate import _
from magento.catalog import Category, Product

class ImportCategory(osv.TransientModel):
    "Import catalog"
    _name = 'magento.instance.import_category'

    def import_category(self, cursor, user, ids, context):
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

        
        customer_ids = self.import_category_tree(cursor, user, instance, context)

        return True

    def import_category_tree(self, cursor, user, instance, context):
        """
        Imports category tree

        :param cursor: Database cursor
        :param user: ID of current user
        :param instance: Browse record of instance
        :param context: Application context
        """
        category_obj = self.pool.get('product.category')

        context.update({
            'magento_instance': instance.id
        })

        with Category(
            instance.url, instance.api_user, instance.api_key
        ) as category_api:
            category_tree = category_api.tree()

            category_obj.create_tree_using_magento_data(
                cursor, user, category_tree, context
            )

    

ImportCategory()
