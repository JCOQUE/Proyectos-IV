from odoo import models, api, registry
from kafka import KafkaConsumer
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
    @api.model
    def consume_messages(self):
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        PEDIDOS = None
        try:
            kafka_server = '172.26.0.4:29093'
            topic_name = 'P00002'
            PEDIDOS = KafkaConsumer(
                topic_name,
                bootstrap_servers=kafka_server,
                auto_offset_reset='latest',
                enable_auto_commit=True,
            )
            for consumer_record in PEDIDOS:
                mensaje_encoded = consumer_record.value
                mensaje = self.decode_message(mensaje_encoded)
                if str(mensaje['sender_ip']) != str(local_ip):
                    self.read_message(mensaje)
        except Exception as e:
            loggerC.error(f"Error en el consumidor: {e}")
        finally:
            if PEDIDOS:
                PEDIDOS.close()

    def decode_message(self, mensaje_encryted):
        #Desencriptacion
        cipher = Cipher(algorithms.AES(self.__key), modes.CBC(self.__iv))
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(mensaje_encryted) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        unpadded_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
        mensaje_decryted = json.loads(unpadded_data.decode('utf-8'))
        
        return mensaje_decryted

    def read_message(self, pedido):
        pedido.pop('sender_ip', None)
        loggerC.critical(pedido)
        loggerC.critical('MENSAJE RECIBIDO CONSUMER')
        try:
            self.add_sale_record(pedido)
        except Exception as e:
            loggerC.error(f"Error al mandar mensaje: {e}")

    
    def add_sale_record(self, pedido):
        api.Environment.manage()              
        with registry(self._cr.dbname).cursor() as new_cr:
            self = self.with_env(self.env(cr=new_cr)).with_context(original_cr=self._cr)
            self.env['sale.order'].sudo().create(pedido)
            new_cr.commit()

    def start_consumer_thread(self):
        threaded_calculation = threading.Thread(target=self.consume_messages)
        threaded_calculation.daemon = True
        threaded_calculation.start()

    def init(self):
        super(KafkaConsumerSaleOrder, self).init()
        self.start_consumer_thread()

