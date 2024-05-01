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
    ID  = None
    send_rec_hardcoded = {'Amazon':'Nike',
                        'Nike':'Amazon'} #sender:receiver

    def set_ID(self, empresa):
        PurchaseOrder.ID = empresa


    def get_ip(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip
    

    def set_sender(self):
        local_ip = self.get_ip()
        with open('/mnt/extra-addons/ipv4_name.json', 'r') as json_file:
            ip_names = json.load(json_file)            
            for ip, empresa in ip_names.items():
                if str(ip) == str(local_ip):
                    self.set_ID(empresa)

    def button_confirm(self):
        # res = super(purchase_custom, self).button_confirm()

        self.set_sender()

        kafka_server = "192.168.0.33:31234" 
        topic_name = self.name
        _logger.critical(f'TOPIC NAME: {topic_name}')

        admin_client = KafkaAdminClient(
            bootstrap_servers=kafka_server,
            client_id='admin'
        )
        self.create_topic(admin_client, topic_name)
        producer = self.create_producer(kafka_server)
        kafka_data = self.create_send_data()
        _logger.critical(kafka_data)
        data_encoded = self.encode_data(kafka_data)
        self.send_data(producer, topic_name, data_encoded)
        admin_client.close()
        return True
    

    def create_topic(self, kafka, topic):
        topic = NewTopic(name=topic, num_partitions=1, replication_factor=1)
        try:
            kafka.create_topics(new_topics=[topic], validate_only=False)
        except Exception as e:
            _logger.error(f"Error creating the topic: {e}")
        


    def create_producer(self, ip):
        producer = KafkaProducer(bootstrap_servers=[ip],
                                 max_block_ms=1048588,
                                 api_version=(2,0,0),
                                 compression_type='gzip')
        return producer
    

    def create_send_data(self):
        send_data = {
            "sender": self.ID,
            "receiver": self.send_rec_hardcoded[self.ID],
            "partner_id": self.partner_id.id,
            "name": self.name,
            "date_order": self.date_order.strftime('%Y-%m-%d'),
            "state": 'sale',  # Establecemos el estado como "Presupuesto" de compra
            "order_line": [],
            "company_id":self.company_id.id,
            "user_id": self.user_id.id,
            "amount_total": 0
        }
        self.add_products(send_data)

        return send_data
        

    def add_products(self, purchase):
        for PRODUCT in self.order_line:
            product_info = {
                "product_id": PRODUCT.product_id.id,
                "name": PRODUCT.name,
                "product_uom_qty": PRODUCT.product_qty,
                "price_unit": PRODUCT.price_unit,
                "tax_id": [(6, 0, PRODUCT.taxes_id.ids)],
                "price_subtotal": PRODUCT.price_subtotal,
                "discount": 0  # No hay campo de descuento en purchase.order, establecemos a 0
            }
            purchase["order_line"].append((0, 0, product_info))
            self.add_product_price(purchase, PRODUCT.price_subtotal)


    def add_product_price(self, purchase, price):
        purchase["amount_total"] += price


    def encode_data(self, data):
        serialized_data = json.dumps(data).encode('utf-8')
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(serialized_data) + padder.finalize()
        cipher = Cipher(algorithms.AES(self.__key), modes.CBC(self.__iv))
        encryptor = cipher.encryptor()
        message_encrypted = encryptor.update(padded_data) + encryptor.finalize()

        return message_encrypted
    

    def send_data(self, producer, topic, data):
        try:
            producer.send(topic, data)
            producer.flush()
        except Exception as e:
            _logger.error(f"Error sending message: {e}")
        finally:
            producer.close()

        _logger.critical(f'DATA SENT: {data}')