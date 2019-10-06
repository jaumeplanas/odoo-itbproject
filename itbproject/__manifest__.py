# Copyright 2018 Jaume Planas
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'ITB Localisation Projects',
    'version': '12.0.0.1.0',
    'summary': 'Localisation projects for ITB',
    'category': 'Projects',
    'author': 'Jaume Planas <jaumeplan@gmail.com>',
    'website': 'https://github.org/jaumeplanas/odoo-itbproject',
    'license': 'LGPL-3',
    'depends': [
        'l10n_es_partner',
        'sale',
    ],
    'data': [
        # Data
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
        'views/export_view.xml',
        'views/account_invoice_report.xml',
        'wizards/wizard_generate_sale_from_tasks_view.xml',
        'wizards/wizard_generate_export_from_tasks.xml',
        # QWeb
        # 'views/account_invoice_report.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'external_dependencies': {
        'python': [],
    }
}
