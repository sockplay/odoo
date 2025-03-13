{
    'name': 'Real Estate',
    'version': '1.0',
    'summary': 'Real Estate Management in Odoo',
    'sequence': 10,
    'author': 'Your Name',
    'category': 'Real Estate',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/real_estate_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}