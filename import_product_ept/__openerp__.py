{
    'name': 'Import Stone Manager Ept',
    'version': '1.0',
    'category': 'products',
    'description': """
This module gives you wizard for import products""",
    'author': 'EmiPro Technologies',
    'website': 'http://emiprotechnologies.com',
    'depends': [
                'base','knowledge','mail','product_stone_search_ept',
                ],
    'update_xml': [ 
                   'view/import_product_view_ept.xml',
                   'view/message_wizard.xml',
                   'view/import_history_ept_view.xml',
                   'security/import_product_security.xml',
                   'security/ir.model.access.csv',
                   #'view/import_stone_directory_view.xml',
                   'view/sys_para_for_inventory_fill.xml',
                   ],
    'installable': True,
    'auto_install': False,
}
