# Copyright 2018 Jaume Planas
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order"

    itb_task_ids = fields.One2many(
        comodel_name="itb.task",
        inverse_name="sale_order",
        string="ITB Tasks",
    )

    # def action_invoice_create(self, cr, uid, ids, grouped=False, states=None,
    #                           date_invoice=False, itb_reference=False,
    #                           context=None):
    #     if states is None:
    #         states = ['confirmed', 'done', 'exception']
    #     res = False
    #     invoices = {}
    #     invoice_ids = []
    #     invoice = self.pool.get('account.invoice')
    #     obj_sale_order_line = self.pool.get('sale.order.line')
    #     partner_currency = {}
    #     # If date was specified, use it as date invoiced, usefull when invoices are generated this month and put the
    #     # last day of the last month as invoice date
    #     if date_invoice:
    #         context = dict(context or {}, date_invoice=date_invoice)
    #     for o in self.browse(cr, uid, ids, context=context):
    #         currency_id = o.pricelist_id.currency_id.id
    #         if (o.partner_id.id in partner_currency) and (
    #             partner_currency[o.partner_id.id] <> currency_id):
    #             raise ValidationError(
    #                 _(
    #                     'You cannot group sales having different currencies for the same partner.'))
    #
    #         partner_currency[o.partner_id.id] = currency_id
    #         lines = []
    #         for line in o.order_line:
    #             if line.invoiced:
    #                 continue
    #             elif (line.state in states):
    #                 lines.append(line.id)
    #         created_lines = obj_sale_order_line.invoice_line_create(cr, uid,
    #                                                                 lines,
    #                                                                 context=context)
    #         if created_lines:
    #             invoices.setdefault(o.partner_invoice_id.id or o.partner_id.id,
    #                                 []).append((o, created_lines))
    #     if not invoices:
    #         for o in self.browse(cr, uid, ids, context=context):
    #             for i in o.invoice_ids:
    #                 if i.state == 'draft':
    #                     return i.id
    #     for val in invoices.values():
    #         if grouped:
    #             res = self._make_invoice(cr, uid, val[0][0],
    #                                      reduce(lambda x, y: x + y,
    #                                             [l for o, l in val], []),
    #                                      context=context)
    #             invoice_ref = itb_reference
    #             origin_ref = ''
    #             for o, l in val:
    #                 if not invoice_ref:
    #                     invoice_ref += (o.client_order_ref or o.name) + '|'
    #                 origin_ref += (o.origin or o.name) + '|'
    #                 self.write(cr, uid, [o.id], {'state': 'progress'})
    #                 cr.execute(
    #                     'insert into sale_order_invoice_rel (order_id,invoice_id) values (%s,%s)',
    #                     (o.id, res))
    #                 self.invalidate_cache(cr, uid, ['invoice_ids'], [o.id],
    #                                       context=context)
    #             if not invoice_ref:
    #                 # remove last '|' in invoice_ref
    #                 if len(invoice_ref) >= 1:
    #                     invoice_ref = invoice_ref[:-1]
    #             if len(origin_ref) >= 1:
    #                 origin_ref = origin_ref[:-1]
    #             invoice.write(cr, uid, [res],
    #                           {'origin': origin_ref, 'name': invoice_ref})
    #         else:
    #             for order, il in val:
    #                 res = self._make_invoice(cr, uid, order, il,
    #                                          context=context)
    #                 invoice_ids.append(res)
    #                 self.write(cr, uid, [order.id], {'state': 'progress'})
    #                 cr.execute(
    #                     'insert into sale_order_invoice_rel (order_id,invoice_id) values (%s,%s)',
    #                     (order.id, res))
    #                 self.invalidate_cache(cr, uid, ['invoice_ids'], [order.id],
    #                                       context=context)
    #     return res
