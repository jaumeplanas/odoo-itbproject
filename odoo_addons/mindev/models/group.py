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


class GroupTree(models.Model):
    _name = 'mindev.group.tree'
    _description = 'MinDev Group Tree'
    _auto = False
    _rec_name = 'xname'
    _order = 'category_txt'

    group_id = fields.Many2one('res.groups', string="Group")
    category_id = fields.Many2one('ir.module.category', string="Category")
    category_txt = fields.Char(string="Category Name")
    xname = fields.Char(string="Name", related='group_id.full_name')
    xml_id = fields.Integer(string="XML ID")
    xml_module = fields.Char(string="XML Module")
    xml_name = fields.Char(string="XML Name")

    def init(self, cr):
        drop_view_if_exists(cr, self._table)
        cr.execute("""
CREATE or REPLACE VIEW %s AS (
    SELECT
        a.id AS id,
        a.id AS group_id,
        a.category_id AS category_id,
        c.name AS category_txt,
        b.id AS xml_id,
        b.module AS xml_module,
        b.name AS xml_name
    FROM
        res_groups a
        LEFT JOIN ir_model_data b ON b.res_id = a.id
        LEFT JOIN ir_module_category c ON a.category_id = c.id
    WHERE
        b.model = 'res.groups'
)""" % (self._table,))
