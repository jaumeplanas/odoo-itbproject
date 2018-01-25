# -*- coding: utf8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError


class SaleMakeInvoice(models.TransientModel):
    _inherit = "sale.make.invoice"

    reference = fields.Char(string="Reference")

    def make_invoices(self, cr, uid, ids, context=None):
        order_obj = self.pool.get('sale.order')
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        newinv = []
        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]
        for sale_order in order_obj.browse(cr, uid,
                                           context.get(('active_ids'), []),
                                           context=context):
            if sale_order.state != 'manual':
                raise ValidationError(_(
                    "You shouldn't manually invoice the following sale order %s") % (
                                      sale_order.name))

        order_obj.action_invoice_create(cr, uid,
                                        context.get(('active_ids'), []),
                                        data['grouped'],
                                        date_invoice=data['invoice_date'],
                                        itb_reference=data['reference'])
        orders = order_obj.browse(cr, uid, context.get(('active_ids'), []),
                                  context=context)
        for o in orders:
            for i in o.invoice_ids:
                newinv.append(i.id)
        # Dummy call to workflow, will not create another invoice but bind the new invoice to the subflow
        order_obj.signal_workflow(cr, uid, [o.id for o in orders if
                                            o.order_policy == 'manual'],
                                  'manual_invoice')
        result = mod_obj.get_object_reference(cr, uid, 'account',
                                              'action_invoice_tree1')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        result['domain'] = "[('id','in', [" + ','.join(map(str, newinv)) + "])]"

        return result
