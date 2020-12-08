# Copyright 2018 Jaume Planas
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from itertools import groupby
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class WizardGenerateSaleFromTask(models.TransientModel):
    _name = "wizard.generate.sale.task"
    _description = "Generate Sales From Tasks Wizard"

    description = fields.Char(string="Description", required=True)
    date = fields.Date(string="Sale Order Date", required=True)
    analytic = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic"
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
    )
    state = fields.Selection(
        selection=[('start', 'start'), ('end', 'end')],
        default="start",
        string="State",
    )
    task_ids = fields.Many2many(
        comodel_name="itb.task",
        )
    line_ids = fields.One2many(
        comodel_name="wizard.generate.sale.task.line",
        inverse_name="wiz_id",
        string="Sale Order Lines",
    )
    itb_export = fields.Many2one(
        comodel_name="itb.export",
        string="ITB Export",
    )

    @api.multi
    def _get_action(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "views": [[False, "form"]],
            "res_id": self.id,
            "target": "new",
        }

    @api.model
    def _get_default_task_ids(self):
        active_ids = self.env.context.get("active_ids", False)
        if not active_ids:
            active_ids = self.env["itb.task"].search([
                ('sale_order', '=', False),
                ('state', 'in', ('open', 'waiting', 'end'))
            ])
        return active_ids.ids

    @api.model
    def default_get(self, fields_list):
        objaaa = self.env['account.analytic.account']
        # objtasks = self.env['itb.task']
        vals = super(WizardGenerateSaleFromTask, self).default_get(
            fields_list=fields_list)
        analytic = objaaa.search([
            ('name', '=', 'EMAPS')
        ], limit=1)
        vals.update(
            date=fields.Date.context_today(self),
            analytic=analytic.id
        )
        active_ids = self._get_default_task_ids()
        if active_ids:
            tasks = self.env["itb.task"].browse(active_ids)
            partner = tasks.mapped("partner")
            if len(partner) != 1:
                raise ValidationError(
                    _(u"Tasks include more than one partner."))
            vals.update(
                task_ids=[(6, 0, active_ids)],
                partner_id=partner.id,
            )
        return vals

    @api.onchange("itb_export")
    def onchange_itb_export(self):
        if self.itb_export:
            self.task_ids = self.itb_export.itb_task_ids
        else:
            self.task_ids = self._get_default_task_ids()

    @api.multi
    def do_generate_lines(self):
        self.ensure_one()
        objlines = self.env["wizard.generate.sale.task.line"]

        for prod, tasks in groupby(
                self.task_ids.sorted(
                    key=lambda r: r.product.id), key=lambda r: r.product):
            tids = [t.id for t in tasks]
            otids = self.env["itb.task"].browse(tids)
            vals = {
                "wiz_id": self.id,
                "product_id": prod.id,
                "name": "Pedido núm.: %s" % self.description,
                "task_ids": tids,
                "qty": sum(otids.mapped("qty"))
            }
            line = objlines.create(vals)
            line.onchange_subtotal()

        self.state = "end"
        return self._get_action()

    @api.multi
    def do_sale(self):
        self.ensure_one()
        objsale = self.env['sale.order']
        objline = self.env['sale.order.line']
        # Create Sale Order
        vals = {
            'partner_id': self.partner_id.id,
            'client_order_ref': self.description,
            'date_order': self.date,
            'analytic_account_id': self.analytic.id,
        }

        sale = objsale.create(vals)
        sale.onchange_partner_id()
        sale.onchange_partner_shipping_id()

        for line in self.line_ids:
            vals = {
                "order_id": sale.id,
                "product_id": line.product_id.id,
                "product_uom_qty": line.qty,
                "name": line.name,
            }
            objline.create(vals)

        # Link tasks to this sale order
        self.task_ids.write({
            'sale_order': sale.id
        })

        # Return action
        res = self.env['ir.actions.act_window'].for_xml_id(
            "sale", "action_quotations")
        res.update(
            res_id=sale.id,
            views=[[False, "form"]],
        )

        return res


class WizardGenerateSaleFromTaskLine(models.TransientModel):
    _name = "wizard.generate.sale.task.line"
    _description = "Generate Sales From Tasks Line Wizard"

    wiz_id = fields.Many2one(
        comodel_name="wizard.generate.sale.task",
        string="Wizard ID",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
    )
    name = fields.Text(
        string="Description",
    )
    qty = fields.Float(
        string="Quantity",
    )
    task_ids = fields.Many2many(
        comodel_name="itb.task",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        default=lambda s: s.env.user.company_id.currency_id,
    )
    subtotal = fields.Monetary(
        string="Subtotal",
    )

    @api.onchange("product_id", "qty")
    def onchange_subtotal(self):
        self.subtotal = round(self.product_id.list_price * self.qty, 2)
