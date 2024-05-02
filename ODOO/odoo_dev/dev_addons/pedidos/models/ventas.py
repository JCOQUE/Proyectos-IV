from odoo import models, api, registry
from kafka import KafkaConsumer
import time
import logging
import threading
import socket
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import hashlib

loggerC = logging.getLogger('consumer')

class KafkaConsumerSaleOrder(models.TransientModel):
    _name = 'kafka.consumer.sale.order'
    __key = hashlib.sha256('admin123'.encode('utf-8')).digest()
    __iv =  hashlib.sha256('admin123'.encode('utf-8')).digest()[:16]
    ID = None

    def init(self):
        super(KafkaConsumerSaleOrder, self).init()
        self.set_receiver()
        self.start_consumer_thread()

    
    def get_ip(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip
    
    
    def get_host_machine_ip(self):
        host_ip = socket.gethostbyname('host.docker.internal')
        return host_ip
    

    def set_ID(self, empresa):
        KafkaConsumerSaleOrder.ID = empresa


    def set_receiver(self):
        local_ip = self.get_ip()
        with open('/mnt/extra-addons/ipv4_name.json', 'r') as json_file:
            ip_names = json.load(json_file)            
            for ip, empresa in ip_names.items():
                if str(ip) == str(local_ip):
                    self.set_ID(empresa)


    def start_consumer_thread(self):
        threaded_calculation = threading.Thread(target=self.consume_messages)
        threaded_calculation.daemon = True
        threaded_calculation.start()

    @api.model
    def consume_messages(self):
        try:
            PEDIDOS = self.connect_kafka()
            for consumer_record in PEDIDOS:
                mensaje_encoded = consumer_record.value
                mensaje = self.decode_message(mensaje_encoded)
                if str(mensaje['receiver']) == self.ID:
                    loggerC.critical(mensaje)
                    loggerC.critical('Processing message...')
                    self.check_agreement(mensaje)
        except Exception as e:
            loggerC.error(f"Error en el consumidor: {e}")
        finally:
            if PEDIDOS:
                PEDIDOS.close()

    def connect_kafka(self):
        host_ip = self.get_host_machine_ip()
        kafka_server = f'{host_ip}:31234'
        topic_name = 'PURCHASES'
        msg = KafkaConsumer(
            topic_name,
            bootstrap_servers=[kafka_server],
            auto_offset_reset='latest',
            enable_auto_commit=True,
        )
        return msg

    def decode_message(self, mensaje_encryted):
        #Desencriptacion
        cipher = Cipher(algorithms.AES(self.__key), modes.CBC(self.__iv))
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(mensaje_encryted) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        unpadded_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
        mensaje_decryted = json.loads(unpadded_data.decode('utf-8'))
        
        return mensaje_decryted
    
    def check_agreement(self, mensaje):
        with open('/mnt/extra-addons/agreement_accepted.json', 'r') as json_file:
            agreement_accepted = json.load(json_file)
            
            if mensaje['sender'] in agreement_accepted[self.ID]:
                loggerC.critical(f'Good! The purchase agreement was already accepted from {self.ID} to {mensaje["sender"]}. Still reading the message...')
                self.read_message(mensaje)
            else:
                loggerC.critical('Purchase agreement either not made yet or previously declined. Stopped from reading the message.')

    def read_message(self, pedido):
        pedido.pop('sender', None)
        pedido.pop('receiver',None)
        try:
            self.add_sale_record(pedido)
            loggerC.critical('Order added to the list successfully!')
        except Exception as e:
            loggerC.error(f"Error al mandar mensaje: {e}")

    
    def add_sale_record(self, pedido):
        api.Environment.manage()              
        with registry(self._cr.dbname).cursor() as new_cr:
            self = self.with_env(self.env(cr=new_cr)).with_context(original_cr=self._cr)
            self.env['sale.order'].sudo().create(pedido)
            new_cr.commit()


    