from odoo import models, fields, api
from kafka import KafkaProducer
import logging
import json
import base64
from kafka.admin import KafkaAdminClient, NewTopic


_logger = logging.getLogger(__name__)

class purchase_custom(models.Model):
    _inherit = 'purchase.order'
    def button_confirm(self):

        # res = super(purchase_custom, self).button_confirm()
        kafka_server = "172.26.0.4:29093" 
        topic_name = self.name
        _logger.info(topic_name)


        admin_client = KafkaAdminClient(
            bootstrap_servers=kafka_server,
            client_id='admin'
        )

        topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)


        try:
            admin_client.create_topics(new_topics=[topic], validate_only=False)
        except Exception as e:
            _logger.error(f"Error al crear el tópico: {e}")


        producer = KafkaProducer(bootstrap_servers=kafka_server,
                                 max_block_ms=1048588,
                                 compression_type='gzip')
        log_data = {
            "Usuario": self.partner_id.name,
            "Pedido": self.name,
            "Referencia Proveedor": self.partner_ref,
            "Moneda": self.currency_id.name,
            "Fecha esperada": self.date_planned.strftime('%Y-%m-%d'),
            "Productos": []
        }


        for product in self.order_line:
            product_info = {
                "Nombre": product.product_id.name,
                "Descripción": product.name,
                "Cantidad": product.product_qty,
                "Recibido": product.qty_received,
                "Facturado": product.qty_invoiced,
                "Precio Unitario": product.price_unit,
                "Impuestos": product.taxes_id.name,
                "Subtotal": product.price_subtotal
            }
            log_data["Productos"].append(product_info)


        json_data = json.dumps(log_data)
        encoded_data = json_data.encode('utf-8')

        try:
            producer.send(topic_name, encoded_data)
            producer.flush()
        except Exception as e:
            _logger.error(f"Error al enviar el mensaje a Kafka: {e}")
        finally:
            producer.close()

        _logger.info(log_data)

        return True