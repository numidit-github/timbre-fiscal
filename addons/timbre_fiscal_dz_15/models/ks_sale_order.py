# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class KsGlobalTaxSales(models.Model):
    _inherit = "sale.order"

    ks_global_tax_rate = fields.Float(string="Universal Tax (%):", readonly=True, default=1.0,
                                      states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    ks_amount_global_tax = fields.Monetary(string='Universal Tax', readonly=True, compute='_amount_all',
                                           track_visibility='always', store=True)
    ks_enable_tax = fields.Boolean(compute='ks_verify_tax')
    is_payment_mode_tax_stamp = fields.Boolean()

    @api.onchange('payment_mode_id')
    def onchange_payment_mode_id(self):
        self.is_payment_mode_tax_stamp = self.payment_mode_id.enable_tax_stamp

    @api.depends('company_id.ks_enable_tax')
    def ks_verify_tax(self):
        for rec in self:
            rec.ks_enable_tax = rec.company_id.ks_enable_tax

    @api.depends('order_line.price_total', 'ks_global_tax_rate', 'is_payment_mode_tax_stamp')
    def _amount_all(self):
        for rec in self:
            ks_res = super(KsGlobalTaxSales, rec)._amount_all()
            if 'ks_amount_discount' in rec:
                rec.ks_calculate_discount()

            rec.ks_calculate_tax()
        return ks_res

    def _prepare_invoice(self):
        for rec in self:
            ks_res = super(KsGlobalTaxSales, rec)._prepare_invoice()
            ks_res['is_payment_mode_tax_stamp'] = rec.is_payment_mode_tax_stamp
            ks_res['ks_global_tax_rate'] = rec.ks_global_tax_rate
            ks_res['ks_amount_global_tax'] = rec.ks_amount_global_tax
        return ks_res

    def ks_calculate_tax(self):
        for rec in self:
            if rec.is_payment_mode_tax_stamp:
                rec.ks_amount_global_tax = (
                    rec.amount_total * rec.ks_global_tax_rate) / 100
            else:
                rec.ks_amount_global_tax = 0.0

            rec.amount_total = rec.ks_amount_global_tax + rec.amount_total

    @api.constrains('ks_global_tax_rate')
    def ks_check_tax_value(self):
        for record in self:
            if record.ks_global_tax_rate > 1 or record.ks_global_tax_rate < 0:
                raise ValidationError(
                    'Vous ne pouvez pas entrer de valeur en pourcentage supérieure à 1%.')


class KsSaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _create_invoice(self, order, so_line, amount):
        invoice = super(KsSaleAdvancePaymentInv, self)._create_invoice(
            order, so_line, amount)
        if invoice:
            invoice['is_payment_mode_tax_stamp'] = order.is_payment_mode_tax_stamp
            invoice['ks_global_tax_rate'] = order.ks_global_tax_rate
            invoice['ks_amount_global_tax'] = order.ks_amount_global_tax
        return invoice
