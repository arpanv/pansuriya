{
    'name': 'Message Form',
    'author': 'Emipro Technologies',
    'version': '0.1',
    'depends': ['base','portal_anonymous', 'account','smsclient'],
    'update_xml':[
		  'view/form_sequence.xml',
                  'view/test.xml',
                  'security/ir.model.access.csv',
                  ],   
    'css': [],
    'images': [],
    'demo': [],
    'installable': True,
    'application': True,
}
