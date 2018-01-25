# -*- coding: utf8 -*-

from collections import Counter
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class WizardGenerateSaleFromTasks(models.TransientModel):
    _name = "wizard.generate.sale.tasks"
    _description = "Generate Sales From Tasks Wizard"

    description = fields.Char(string="Description", required=True)
    date = fields.Date(string="Sale Order Date", required=True)
    product = fields.Many2one(comodel_name="product.product", string="Product",
                              required=True)
    task_ids = fields.Many2many(comodel_name="itb.task", column1="wizard_id",
                                column2="task_id")
    quantity = fields.Float(string="Quantity", digits=(16, 2), required=True)
    currency = fields.Many2one(comodel_name="res.currency")
    price = fields.Float(string="Price", digits=(16, 2))

    @api.model
    def default_get(self, fields_list):
        vals = super(WizardGenerateSaleFromTasks, self).default_get(
            fields_list=fields_list)
        tasks = self.env['itb.task'].search([
            ('sale_order', '=', False)
        ])
        product = None
        if len(tasks) > 0:
            c = Counter(tasks.mapped('product'))
            if c:
                product = c.most_common(1)[0][0]
            a = Counter(tasks.mapped('analytic'))
            if a:
                analytic = a.most_common(1)[0][0]
            task_ids = [(6, False, [x.id for x in tasks])]
            currency = self.env.user.company_id.currency_id
            vals.update(task_ids=task_ids,
                        product=product.id if c else False, currency=currency.id,
                        project_id=analytic.id if a else False)
        vals.update(date=fields.Date.today())
        return vals

    @api.model
    def _calculate_price(self, product, quantity):
        price = 0.0
        if product and quantity > 0.0:
            price = round(product.list_price * quantity, 2)
        return price

    @api.onchange("task_ids")
    def onchange_task_ids(self):
        self.quantity = round(sum(self.task_ids.mapped('qty')), 2)
        self.price = self._calculate_price(self.product, self.quantity)

    @api.onchange("product", "quantity")
    def onchange_product_quantity(self):
        self.price = self._calculate_price(self.product, self.quantity)

    @api.multi
    def do_sale(self):
        objsale = self.env['sale.order']
        objline = self.env['sale.order.line']
        self.ensure_one()
        p = self.task_ids.mapped('partner')
        if len(p) != 1:
            raise ValidationError(_(u"Tasks include more than one partner."))
        # Create Sale Order
        vals = {
            'partner_id': p[0].id,
            'client_order_ref': self.description,
            'date_order': self.date,
            'order_line': [(0, False, {
                'product_id': self.product.id,
                'name': u"Pedido núm.: %s" % self.description,
                'product_uom_qty': self.quantity,
            })]

        }
        sale = objsale.create(vals)
        sale.onchange_partner_id(p[0].id)
        # Link tasks to this sale order
        self.task_ids.write({
            'sale_order': sale.id
        })

        # Return action
        res = self.env['ir.actions.act_window'].for_xml_id("sale",
                                                           "action_quotations")
        res.update(views=[[False, "form"]], res_id=sale.id)

        return res
