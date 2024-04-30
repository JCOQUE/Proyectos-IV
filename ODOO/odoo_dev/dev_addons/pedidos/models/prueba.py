from odoo import models, api, registry, SUPERUSER_ID
import logging

l = logging.getLogger('log')
l.critical('HOOOOOOOOOOOOOOOOOOOOLAAAAAAAAAAAAAAAAAA')


class Prueba(models.Model):
    _name = 'pedidos.prueba'
    l.critical('HOOOOOOOOOOOOOOOOOOOOLAAAAAAAAAAAAAAAAAA')

    def module_init(cr, registry):
        l.critical('HOOOOOOOOOOOOOOOOOOOOLAAAAAAAAAAAAAAAAAA')
        env = api.Environment(cr, SUPERUSER_ID, {})
        caller = env['kafka.consumer.sale.order']
        # Execute the desired code here
        caller.init()