from odoo import models, fields, api
import logging 

_logger = logging.getLogger('producer')
class purchase_agreement(models.Model):
    _name = 'purchase_agreement.purchase_agreement'
    _description = 'purchase_agreement.purchase_agreement'

    name = fields.Char()
    
    def send_pa(self):
        _logger.critical('PUUUUUUUURCHAAAAAAAAAAAAAAASE')