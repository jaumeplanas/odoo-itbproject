# Copyright 2018 Jaume Planas
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields


class ITBProject(models.Model):
    _name = "itb.project"
    _description = "ITB Project"

    name = fields.Char(string="Name", required=True)
    ref = fields.Char(string="Reference")
    manager = fields.Many2one(
        comodel_name="res.users",
        string="Default Manager",
    )
    translator = fields.Many2one(
        comodel_name="res.users",
        string="Default Translator",
    )
    partner = fields.Many2one(
        comodel_name="res.partner",
        string="Default Partner",
    )
    product = fields.Many2one(
        comodel_name="product.product",
        string="Default Product",
    )
    analytic = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic Account",
    )
    task_ids = fields.One2many(
        comodel_name="itb.task",
        inverse_name="project",
        string="Tasks",
    )
