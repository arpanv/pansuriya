{
    'name': 'Magento Integration Extended',
    'author': 'Emipro Technologies',
    'version': '0.1',
    'depends': ['magento_integration','product_stone_search_ept'],
    'update_xml':[
                  'view/store.xml',
                  'wizard/import_customer.xml',
                  'wizard/import_category.xml',
                  'view/magento_website.xml',
                  'view/res_partner_view.xml',
                  'view/magento_instance_extended.xml',
                  'view/magento_sync_cron_ept.xml',
                  'view/sys_para_for_export_catelog.xml',
                  'view/m_i_w_export_catalog_extended.xml',
                  'view/sale_order_button_extended_ept.xml',
		  'view/stone_form_view_extended_ept.xml',
		  'wizard/auction_form.xml',
                  ],
    'category': 'Specific Industry Applications',
    'summary': 'Magento Integration',
    'description': """Extended Magento Integration.""",    
    'css': [],
    'images': [],
    'demo': [],
    'installable': True,
    'application': True,
}
