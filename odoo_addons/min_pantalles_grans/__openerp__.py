# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Minorisa Pantalles Grans',
    'version': '8.0.1.0.1',
    'category': 'Web',
    'sequence': 6,
    'summary': 'Pantalles grans pel odoo 8',
    'description': """
        Pantalles grans pel odoo 8
    """,
    'author': 'Minorisa',
    'depends': ['base','web'],
    'installable': True,
    'application': False,
    "data": [
        "views/qweb.xml",
    ],
    
    'qweb': [
    ],
    'js': [ 

    ],
    'css':[
        'static/src/css/base.css',
    ],
    
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: