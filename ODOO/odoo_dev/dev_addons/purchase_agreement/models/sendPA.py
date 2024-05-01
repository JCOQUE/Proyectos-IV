from odoo import models, fields, api
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
import logging 
import json 
import hashlib
import socket
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

_logger = logging.getLogger('producer')

class purchase_agreement(models.Model):
    _name = 'purchase_agreement.purchase_agreement'
    _description = 'purchase_agreement.purchase_agreement'
    __key = hashlib.sha256('admin123'.encode('utf-8')).digest()
    __iv =  hashlib.sha256('admin123'.encode('utf-8')).digest()[:16]
    ID = None

    def set_ID(self, empresa):
        purchase_agreement.ID = empresa

    name = fields.Char()
    
    def send_pa(self):
        self.set_sender()
        receiver = self.get_receiver()

        kafka_server = "192.168.0.33:31234" 
        topic_name = 'PA'
        _logger.critical(f'TOPIC NAME: {topic_name}')

        admin_client = KafkaAdminClient(
            bootstrap_servers=kafka_server,
            client_id='admin'
        )
        self.create_topic(admin_client, topic_name)
        producer = self.create_producer(kafka_server)
        kafka_data = self.create_send_data(receiver)
        data_encoded = self.encode_data(kafka_data)
        self.send_data(producer, topic_name, data_encoded)
        admin_client.close()
        return True
    
    
    def set_sender(self):
        local_ip = self.get_ip()
        with open('/mnt/extra-addons/ipv4_name.json', 'r') as json_file:
            ip_names = json.load(json_file)
            _logger.critical(ip_names)
            
            for ip, empresa in ip_names.items():
                if str(ip) == str(local_ip):
                    self.set_ID(empresa)

    
    def get_receiver(self):
        receiver = None
        for receiver in self:
            receiver = receiver.name
        return receiver
    

    def get_ip(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip  
    

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
    

    def create_send_data(self, receiver):
        send_data = {
            "type": 'PA',
            'sender': str(self.ID),
            'receiver': receiver           
        }
        return send_data
    

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