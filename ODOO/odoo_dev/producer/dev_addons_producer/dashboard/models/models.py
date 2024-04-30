from odoo import models, fields, api


class Dashboard(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'