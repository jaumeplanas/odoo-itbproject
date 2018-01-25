# -*- coding: utf8 -*-

from openerp import models, fields, api, _

STATES = [
    ('draft', _("Draft")),
    ('open', _("Open")),
    ('waiting', _("Waiting")),
    ('end', _("End")),
    ('cancel', _("Cancelled")),
]


class ITBTask(models.Model):
    _name = "itb.task"
    _description = "ITB Task"
    _inherit = ['mail.thread']

    @api.depends("date_end", "date_end_planned")
    def _get_date_end_computed(self):
        for r in self:
            r.date_end_computed = r.date_end or r.date_end_planned

    name = fields.Char(string="Name", required=True)
    state = fields.Selection(selection=STATES, string="State", required=True,
                             track_visibility="onchange")
    project = fields.Many2one(comodel_name="itb.project", string="Project",
                              required=True)
    shipment = fields.Char(string="Shipment", required=True)
    product = fields.Many2one(comodel_name="product.product", string="Product",
                              required=True)
    qty = fields.Float(string="Actual Quantity", required=True, digits=(16, 2))
    qty_cfm = fields.Float(string="CFM Quantity", digits=(16, 2))
    manager = fields.Many2one(comodel_name="res.users", required=True)
    translator = fields.Many2one(comodel_name="res.users", required=True)
    partner = fields.Many2one(comodel_name="res.partner", required=True)
    analytic = fields.Many2one("account.analytic.account",
                               string="Analytic Account")
    date_received = fields.Date(string="Received Date")
    date_start = fields.Date(string="Start Date")
    date_end_planned = fields.Date(string="Planned End Date")
    date_end = fields.Date(string="End Date")
    date_end_computed = fields.Date(string="End Date",
                                    compute=_get_date_end_computed, store=True)
    notes = fields.Html(string="Notes")
    sale_order = fields.Many2one(comodel_name="sale.order")

    @api.model
    def default_get(self, fields_list):
        res = super(ITBTask, self).default_get(fields_list=fields_list)
        res.update(state='draft')
        return res

    @api.onchange("project", "shipment")
    def onchange_project_name(self):
        if self.project and self.shipment:
            self.name = "%s_%s" % (self.project.name, self.shipment)

    @api.onchange("project")
    def onchange_project(self):
        if self.project:
            self.product = self.project.product
            self.manager = self.project.manager
            self.translator = self.project.translator
            self.partner = self.project.partner
            self.analytic = self.project.analytic

    @api.multi
    def set_open(self):
        if not self.date_start:
            self.date_start = fields.Date.today()
        self.state = 'open'

    @api.multi
    def set_waiting(self):
        self.state = 'waiting'

    @api.multi
    def set_end(self):
        if not self.date_end:
            self.date_end = fields.Date.today()
        self.state = 'end'

    @api.multi
    def set_draft(self):
        if not self.date_received:
            self.date_received = fields.Date.today()
        self.state = 'draft'

    @api.multi
    def set_cancelled(self):
        self.state = 'cancel'
