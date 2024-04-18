from odoo import models, api, registry
from kafka import KafkaConsumer
import logging
import threading
import socket
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
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
            for mensaje in PEDIDOS:
                loggerC.critical(f'MENSAJE:{mensaje.value}')
                cipher = Cipher(algorithms.AES(self.__key), modes.CBC(self.__iv))
                decryptor = cipher.decryptor()
                decrypted_padded_data = decryptor.update(mensaje.value) + decryptor.finalize()
                unpadder = padding.PKCS7(128).unpadder()
                unpadded_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
                pedido_dict = json.loads(unpadded_data.decode('utf-8'))
                if str(pedido_dict['sender_ip']) != str(local_ip):
                    pedido_dict.pop('sender_ip', None)
                    loggerC.critical(pedido_dict)
                    loggerC.critical('MENSAJE RECIBIDO CONSUMER')
                    try:
                        api.Environment.manage()
                        
                        with registry(self._cr.dbname).cursor() as new_cr:
                            self = self.with_env(self.env(cr=new_cr)).with_context(original_cr=self._cr)
                            nuevo_pedido = self.env['sale.order'].sudo().create(pedido_dict)
                            new_cr.commit()
                    except Exception as e:
                        loggerC.error(f"Error al mandar mensaje: {e}")
        except Exception as e:
            loggerC.error(f"Error en el consumidor: {e}")
        finally:
            if PEDIDOS:
                PEDIDOS.close()

    def start_consumer_thread(self):
        threaded_calculation = threading.Thread(target=self.consume_messages)
        threaded_calculation.daemon = True
        threaded_calculation.start()

    def init(self):
        super(KafkaConsumerSaleOrder, self).init()
        self.start_consumer_thread()

