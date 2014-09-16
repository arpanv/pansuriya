{
    "name" : "Stone Request Manager",
    "version" : "1.0",
    "author" : "Emipro Technologies",
    'website': 'http://www.emiprotechnologies.com',
    'category': 'Product',    
    "depends" : ["stock"],
    "init_xml" : [],
    "demo_xml" : [],
    "description": 
    """ 
    This module help you to manage internal movement of stone
    with interaction of .NET application.
    """,
    "update_xml" : [
                    'product_in_quote_view.xml',
                    'security/ir.model.access.csv',
                    'stone_request_view.xml',
                    'stock_internal_move_view_ept.xml',
                    'stock_tally_view.xml',
                    ],
    """'view_picking_form_inherit_ept.xml',"""
    "auto_install": False,
    "installable": True,
    "certificate" : "",
}

