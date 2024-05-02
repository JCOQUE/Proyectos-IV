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
import os

loggerC = logging.getLogger('consumer')

class receivePA(models.TransientModel):
    _name = 'receive.pa'
    _name = 'receiver.pa'
    __key = hashlib.sha256('admin123'.encode('utf-8')).digest()
    __iv =  hashlib.sha256('admin123'.encode('utf-8')).digest()[:16]
    ID = None
    flag = True



    def get_ip(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip 
    

    def get_host_machine_ip(self):
        host_ip = socket.gethostbyname('host.docker.internal')
        return host_ip
    

    def set_flag(self, value):
        receivePA.flag = value


    def set_ID(self, empresa):
        receivePA.ID = empresa


    def set_receiver(self):
        local_ip = self.get_ip()
        with open('/mnt/extra-addons/ipv4_name.json', 'r') as json_file:
            ip_names = json.load(json_file)
            loggerC.critical(ip_names)
            for ip, empresa in ip_names.items():
                if str(ip) == str(local_ip):
                    self.set_ID(empresa)
    

    def init(self):
        if self.flag:
            #super(receivePA, self).init()
            self.set_receiver()
            self.start_consumer_thread()
            self.set_flag(False)


    def start_consumer_thread(self):
        self.set_flag(True)
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
        topic_name = 'PurchAgr'
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
        with open('/mnt/extra-addons/would_accept.json', 'r') as json_file:
            would_accept = json.load(json_file)
            
            if mensaje['sender'] in would_accept[self.ID]:
                already_accepted = self.add_acceptance(mensaje['sender'])
                if already_accepted:
                    loggerC.critical('Purchase agreement already made')
                else:
                    loggerC.critical('Purchase agreement accepted!')
            else:
                loggerC.critical('Purchase agreement declined.')
    

    def add_acceptance(self, sender):
        with open('/mnt/extra-addons/agreement_accepted.json', 'r') as json_file:
            accepted = json.load(json_file)
            if sender in accepted[self.ID]:
                return True
            else:
                accepted[self.ID].append(sender)
                self.update_accepted(accepted)
                return False
            
    def update_accepted(self, accepted):
        with open('/mnt/extra-addons/agreement_accepted.json', 'w') as json_file:
            json.dump(accepted, json_file)



    