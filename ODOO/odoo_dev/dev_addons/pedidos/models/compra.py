from odoo import models, fields, api
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
import logging
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import hashlib

import socket


_logger = logging.getLogger('producer')
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    __key = hashlib.sha256('admin123'.encode('utf-8')).digest()
    __iv =  hashlib.sha256('admin123'.encode('utf-8')).digest()[:16]
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
        kafka_data = {
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
            kafka_data["order_line"].append((0, 0, product_info))

        #Encriptación    
        kafka_data["amount_total"] = amount_total
        serialized_data = json.dumps(kafka_data).encode('utf-8')
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(serialized_data) + padder.finalize()
        cipher = Cipher(algorithms.AES(self.__key), modes.CBC(self.__iv))
        encryptor = cipher.encryptor()
        message_encrypted = encryptor.update(padded_data) + encryptor.finalize()


        try:
            producer.send(topic_name, message_encrypted)
            producer.flush()
        except Exception as e:
            _logger.error(f"Error al enviar el mensaje a Kafka: {e}")
        finally:
            producer.close()

        _logger.critical(message_encrypted)

        return True