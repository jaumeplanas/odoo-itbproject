# -*- coding: utf8 -*-

from openerp import models, fields


class SaleMakeInvoice(models.Model):
    _inherit = "sale.make.invoice"

    reference = fields.Char(string="Reference")
