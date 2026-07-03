# -*- coding: utf-8 -*-
{
    'name': 'Google Shopping Feed Enterprise',
    'version': '17.0.1.0.0',
    'summary': 'Enterprise-grade Google Shopping Feed with multi-company license control.',
    'description': """
Google Shopping Feed Enterprise extends the standard Pro package with premium multi-company license management, dedicated enterprise enablement, and optional priority support.
""",
    'category': 'Website',
    'author': 'Mouadh',
    'license': 'OPL-1',
    'price': 299.00,
    'currency': 'EUR',
    'support': 'support@mouadh.dz',
    'website': 'https://github.com/mouadh25/google-shopping-odoo-module',
    'depends': [
        'google_shopping_feed',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/company_views.xml',
    ],
    'installable': True,
    'application': False,
}
