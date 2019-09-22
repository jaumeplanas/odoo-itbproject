# Copyright 2018 Jaume Planas
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api


class ITBExport(models.Model):
    _name = "itb.export"
    _description = "ITB Export"

    name = fields.Char(
        string="Name",
        required=True,
    )
    date = fields.Date(
        string="Date",
        default=fields.Date.context_today,
    )
    itb_task_ids = fields.One2many(
        comodel_name="itb.task",
        inverse_name="itb_export",
        string="ITB Tasks",
    )

    @api.model
    def create_xlsx(self, tasks):
        pass
