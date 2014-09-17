
{
    'name': 'Product Extended',
    'version': '1.0',
    'category': 'Product Extension',
    "sequence": 14,
    'complexity': "normal",
    'description': """
    Product Screen extended and product advance search filter added
    """,
    'author': 'Emipro Technologies',
    'website': 'http://www.emiprotechnologies.com',
    'images': [],
    'depends': ['stock','sale_stock'],
    'init_xml': [],
    'update_xml': [
                    'view/product_stone_view_extend.xml',
                    'view/product_search_view.xml',
                    'view/product_view_extand.xml',
                    'security/ir.model.access.csv',
                    'view/product_configuration_menu.xml',
                    'view/product_category_view.xml',
                    'view/config_key_view.xml',   
                    'view/wizard_view_sale_discount.xml',              
                    'view/view_sale.xml',
                    'view/view_invoice.xml',
                    'view/view_res_company.xml',
                    'view/product_stone_view_extended_ept.xml',
		    'view/product_fields_master_file.xml',
                   ],
    'demo_xml': [],
    'data' : [ 
	      
	     ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
