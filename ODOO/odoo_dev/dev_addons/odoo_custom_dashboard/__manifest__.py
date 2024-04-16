# -*- coding: utf-8 -*-
{
    'name' : 'Panel de control',
    'version' : '1.0',
    'summary': 'ERP-BI',
    'sequence': -1,
    'description': """Panel de control personalizado ERP-BI""",
    'category': 'Dashboard',
    'depends' : ['base', 'web', 'sale', 'board','purchase'],
    'data': [
        'views/sales_dashboard.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'odoo_custom_dashboard/static/src/components/**/*.js',
            'odoo_custom_dashboard/static/src/components/**/*.xml',
            'odoo_custom_dashboard/static/src/components/**/*.scss',
        ],
    },
}
