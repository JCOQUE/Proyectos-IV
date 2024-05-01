from odoo import models, fields, api


class purchase_agreement(models.Model):
    _name = 'purchase_agreement.purchase_agreement'
    _description = 'purchase_agreement.purchase_agreement'

    name = fields.Char()
    
