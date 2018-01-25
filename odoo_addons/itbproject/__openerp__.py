{
    'name': 'ITB Localisation Projects',
    'version': '8.0.1.0.2',
    'summary': 'Localisation projects for ITB',
    # 'description': '',
    'category': '',
    'author': 'Jaume Planas <jaumeplan@gmail.com>',
    'website': 'https://bitbucket.org/itberga/odoo8-addon-itbproject',
    'license': 'GPL-3',
    'depends': [
        'base',
        'l10n_es_partner',
        'sale',
        'web_readonly_bypass',
    ],
    'data': [
        # Data
        # 'data/base_data.xml',
        'data/product_data.xml',
        # Security
        'security/itbproject_groups.xml',
        'security/ir.model.access.csv',
        # Menus
        'views/menus.xml',
        # Views
        'views/project_view.xml',
        'views/task_view.xml',
        'views/sale_view.xml',
        # 'views/sale_make_invoice_view.xml',
        'wizards/wizard_generate_sale_from_tasks_view.xml',
        'wizards/sale_make_invoice_view.xml',
        # QWeb
        'views/account_invoice_report.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'external_dependencies': {
        'python': [],
    }
}
