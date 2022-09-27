# -*- coding: utf-8 -*-
{
    'name': 'Profit Report',
    'version': '14.0',
    'summary': 'This Module Help us to get Profit Report of daily/party wise/Brand wise',
    'sequence': -100,
    'description': """Brothers Today Daily Daily/Party wise/Brand wise""",
    'category': '',
    'website': 'https://www.enzapps.com',
    'depends': ['base', 'account','ezp_cash_collection'],
    'images': ['static/description/logo.png'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/sale.xml',
        'report/report.xml',
        'report/sales_report_view.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
