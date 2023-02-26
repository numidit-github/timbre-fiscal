from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Company(models.Model):
    _inherit = "res.company"

    ks_enable_tax = fields.Boolean(string="Activater le Timbre Fiscal")
    ks_sales_tax_account = fields.Many2one('account.account', string="Compte de taxe des ventes")
    ks_purchase_tax_account = fields.Many2one('account.account', string="Compte de taxe des achats")


class KsResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ks_enable_tax = fields.Boolean(string="Activater le Timbre Fiscal", related='company_id.ks_enable_tax', readonly=False)
    ks_sales_tax_account = fields.Many2one('account.account', string="Compte de taxe des ventes", related='company_id.ks_sales_tax_account', readonly=False)
    ks_purchase_tax_account = fields.Many2one('account.account', string="Compte de taxe des achats", related='company_id.ks_purchase_tax_account', readonly=False)
