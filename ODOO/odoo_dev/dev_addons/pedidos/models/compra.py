from odoo import models, fields, api
from kafka import KafkaProducer
import logging
import json
import base64
from kafka.admin import KafkaAdminClient, NewTopic
import socket
import ast


_logger = logging.getLogger('producer')
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

class PurchasOrder(models.Model):
    _inherit = 'purchase.order'
    def button_confirm(self):

        # res = super(purchase_custom, self).button_confirm()
        kafka_server = "172.26.0.4:29093" 
        topic_name = self.name
        _logger.critical(topic_name)


        admin_client = KafkaAdminClient(
            bootstrap_servers=kafka_server,
            client_id='admin'
        )

        topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)


        try:
            admin_client.create_topics(new_topics=[topic], validate_only=False)
        except Exception as e:
            _logger.error(f"Error al crear el tÃ³pico: {e}")


        producer = KafkaProducer(bootstrap_servers=kafka_server,
                                 max_block_ms=1048588,
                                 compression_type='gzip')
        log_data = {
            "sender_ip": local_ip,
            "partner_id": self.partner_id.id,
            "name": self.name,
            "date_order": self.date_order.strftime('%Y-%m-%d'),
            "state": 'sale',  # Establecemos el estado como "Presupuesto" de compra
            "order_line": [],
            "company_id":self.company_id.id,
            "user_id": self.user_id.id,
        }
        
        amount_total = 0
        for line in self.order_line:
            product_info = {
                "product_id": line.product_id.id,
                "name": line.name,
                "product_uom_qty": line.product_qty,
                "price_unit": line.price_unit,
                "tax_id": [(6, 0, line.taxes_id.ids)],
                "price_subtotal": line.price_subtotal,
                "discount": 0  # No hay campo de descuento en purchase.order, establecemos a 0
            }
            amount_total += line.price_subtotal
            log_data["order_line"].append((0, 0, product_info))
        log_data["amount_total"] = amount_total
        json_data = json.dumps(log_data)
        encoded_data = json_data.encode('utf-8')

        try:
            producer.send(topic_name, encoded_data)
            producer.flush()
        except Exception as e:
            _logger.error(f"Error al enviar el mensaje a Kafka: {e}")
        finally:
            producer.close()

        _logger.critical(log_data)

        return True