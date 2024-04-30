from odoo import models, api,registry
from kafka import KafkaConsumer
import logging
import threading
import socket
import json

loggerC = logging.getLogger('consumer')

class KafkaConsumerSaleOrder(models.TransientModel):
    _name = 'kafka.consumer.sale.order'

    @api.model
    def consume_messages(self):
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        PEDIDOS = None
        try:
            kafka_server = '172.26.0.4:29093'
            topic_name = 'P00004'
            PEDIDOS = KafkaConsumer(
                topic_name,
                bootstrap_servers=kafka_server,
                auto_offset_reset='latest',
                enable_auto_commit=True,
            )
            for mensaje in PEDIDOS:
                loggerC.critical('MENSAJE RECIBIDO CONSUMER')
                pedido_str = mensaje.value.decode('utf-8')
                pedido_dict = json.loads(pedido_str)
                if str(pedido_dict['sender_ip']) != str(local_ip):
                    pedido_dict.pop('sender_ip', None)
                    loggerC.critical(pedido_dict)
                PEDIDOS.close()
        except Exception as e:
            loggerC.error(f"Error en el consumidor: {e}")
        try:
            #doc: https://www.odoo.com/es_ES/forum/ayuda-1/unable-to-use-a-closed-cursor-and-thread-111086
            api.Environment.manage()

            new_cr = registry(self._cr.dbname).cursor()
            new_cr.autocommit(True)
            self = self.with_env(self.env(cr=new_cr)).with_context(original_cr=self._cr)
            nuevo_pedido = self.env['sale.order'].sudo().create(pedido_dict)
            loggerC.critical("PEDIDO INSERTADO")
        except Exception as e:
            loggerC.error(f"Error al mandar mensaje: {e}")


    def start_consumer_thread(self):
        threaded_calculation = threading.Thread(target=self.consume_messages)
        threaded_calculation.daemon = True
        threaded_calculation.start()

    def init(self):
        super(KafkaConsumerSaleOrder, self).init()
        self.start_consumer_thread()
