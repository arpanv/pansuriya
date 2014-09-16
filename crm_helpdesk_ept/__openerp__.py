
{
    'name': 'Extension of Helpdesk Module',
    'version': '1.0',
    'category': 'Employee Extension',
    "sequence": 14,
    'complexity': "normal",
    'description': """
    Manages Reply-to related details.
    """,
    'author': 'Emipro Technologies',
    'website': 'http://www.emiprotechnologies.com',
    'images': [],
    'depends': ['crm_helpdesk'],
    'init_xml': [],
    'update_xml': [
                   'crm_case_section_view.xml',
                   'server_action.xml',
                   ],
    'demo_xml': [],
    'data' : [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
