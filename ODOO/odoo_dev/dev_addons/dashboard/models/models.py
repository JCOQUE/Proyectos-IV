from odoo import models, fields, api


class dashboard(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'