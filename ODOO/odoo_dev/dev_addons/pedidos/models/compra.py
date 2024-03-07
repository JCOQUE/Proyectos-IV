from odoo import models, fields, api
from kafka import KafkaProducer
import logging
import json
import base64

_logger = logging.getLogger(__name__)
# Crear una instancia del productor de Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                        max_block_ms=1048588,
                        compression_type='gzip')


class purchase_custom(models.Model):

    _inherit = 'purchase.order'

    def button_confirm(self):

        res = super(purchase_custom, self).button_confirm()

        # Crear un mensaje de log con los datos del usuario
        log_message = f"Usuario: {self.partner_id}"
        log_message += f"\nPedido: {self.name}"
        log_message += f"\nReferencia Proveedor: {self.partner_ref}"
        log_message += f"\nMoneda: {self.currency_id.name}"
        log_message += f"\nFecha confirmación: {self.date_approve}"
        log_message += f"\nFecha esperada: {self.date_planned}"     
        log_message += f"\nFecha esperada: {self.date_planned}"

        log_message += f"\nProducto:"
        for product in self.order_line:
            log_message += f"\n\tNombre: {product.product_id.name}"
            log_message += f"\n\tDescripción: {product.name}"
            log_message += f"\n\tCantidad: {product.product_qty}"
            log_message += f"\n\tRecibido: {product.qty_received}"
            log_message += f"\n\tFacturado: {product.qty_invoiced}"
            log_message += f"\n\tPrecio Unitario: {product.price_unit}"
            log_message += f"\n\tImpuestos: {product.taxes_id.name}"
            log_message += f"\n\tSubtotal: {product.price_subtotal}"

        _logger.info(log_message)

        return res 
    


