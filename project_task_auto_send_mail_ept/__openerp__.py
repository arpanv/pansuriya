{
    'name': 'Auto email send at creation of new task',
    'version': '1.0',
    'category': 'Normal',
    'description': """
If any new task is create than the user who assigned that task is notify with email 
""",
    'author': 'Emipro Technologies',
    'maintainer': 'Emipro Technologies',
    'website': 'http://www.emiprotechnologies.com',
    'depends': ['base','project','mail'],
    'update_xml':[
        'view/project_task_email_template_ept.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}

