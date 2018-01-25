# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2011-TODAY MINORISA (http://www.minorisa.net)
#                             All Rights Reserved.
#                             Minorisa <contact@minorisa.net>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Minorisa Development',
    'summary': 'Development Utilities',
    'category': 'Extra Tools',
    'images': [],
    'version': '8.0.1.0.1',
    'author': 'Minorisa SA',
    'support': 'projectes-odoo@minorisa.net',
    'website': 'https://www.minorisa.net',
    'license': 'GPL-3',
    'depends': [
        'base',
    ],
    'data': [
        # Security
        'security/mindev_groups.xml',
        'security/ir.model.access.csv',
        # Root menu
        'views/min_dev_menu.xml',
        # Menu
        'views/menu.xml',
        'views/group.xml',
        'views/download_translations_view.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
}
