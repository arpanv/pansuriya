{
    'name': 'Website for Ocentag',
    'category': 'Website',
    'summary': 'Website module enhancement for Ocentag',
    'version': '1.0',
    'description': """
Website module enhancement for Ocentag
        """,
    'author': 'Emipro Technologies',
    'depends': ['website','product_stone_search_ept','stone_bid_ept','res_partner_ept'],
    'data': [
        'data/website_test_data.xml',
        'views/website_test.xml',
    ],
    'installable': True,
    'auto_install': False,
}
