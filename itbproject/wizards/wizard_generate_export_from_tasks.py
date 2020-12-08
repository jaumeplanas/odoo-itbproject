# Copyright 2018 Jaume Planas
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api


class WizardGenerateExportFromTasks(models.TransientModel):
    _name = "wizard.generate.export.tasks"
    _description = "Generate Export From Tasks Wizard"

    name = fields.Char(string="Name")
    date = fields.Date(string="Date")
    itb_task_ids = fields.Many2many(
        comodel_name="itb.task",
        string="ITB Tasks",
    )

    @api.model
    def default_get(self, fields_list):
        res = super(
            WizardGenerateExportFromTasks, self).default_get(fields_list)
        res.update(date=fields.Date.context_today(self))
        active_ids = self.env.context.get("active_ids", False)
        if not active_ids:
            active_ids = self.env["itb.task"].search([
                ('itb_export', '=', False),
                ('state', 'in', ('open', 'waiting', 'end'))
            ]).ids
        if active_ids:
            res.update(itb_task_ids=[(6, 0, active_ids)])

        return res

    @api.multi
    def generate_export(self):
        self.ensure_one()
        export = self.env["itb.export"].sudo().create({
            'name': self.name,
            'date': self.date,
            'itb_task_ids': [(6,0, self.itb_task_ids.ids)]
        })
        self.itb_task_ids.write({
            'itb_export': export.id,
        })
