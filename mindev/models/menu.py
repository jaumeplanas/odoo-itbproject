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

from openerp import models, fields, api
from openerp.tools import drop_view_if_exists


class MenuTree(models.Model):
    _name = 'mindev.menu.tree'
    _description = 'MinDev Menu Tree'
    _auto = False
    _rec_name = 'xname'
    _order = "sequence"

    menu_id = fields.Many2one('ir.ui.menu', string="Menu")
    xname = fields.Char(string="Name", related='menu_id.name')
    xml_id = fields.Integer(string="XML ID")
    xml_module = fields.Char(string="XML Module")
    xml_name = fields.Char(string="XML Name")
    sequence = fields.Integer(string="Sequence")
    parent_id = fields.Integer(string="Parent ID")
    parent_left = fields.Integer(string="Parent Left")
    parent_right = fields.Integer(string="Parent Right")
    child_id = fields.One2many('mindev.menu.tree', 'parent_id', string="Child IDS")

    def init(self, cr):
        drop_view_if_exists(cr, self._table)
        cr.execute("""
CREATE or REPLACE VIEW %s AS (
    SELECT
        a.id AS id,
        b.res_id AS menu_id,
        b.id AS xml_id,
        b.module AS xml_module,
        b.name AS xml_name,
        a.sequence AS sequence,
        a.parent_id AS parent_id,
        a.parent_left AS parent_left,
        a.parent_right AS parent_right
    FROM
        ir_ui_menu a
        LEFT JOIN ir_model_data b ON b.res_id = a.id
    WHERE
        b.model = 'ir.ui.menu'
)""" % (self._table,))
