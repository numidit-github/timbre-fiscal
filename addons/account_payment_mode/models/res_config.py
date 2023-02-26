from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Company(models.Model):
    _inherit = "res.company"

    payement_mode_account_confirm_force = fields.Boolean(
        string="Forcer la selection du mode de paiement à la confirmation de la facture")


class KsResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    payement_mode_account_confirm_force = fields.Boolean(
        related='company_id.payement_mode_account_confirm_force', readonly=False)
