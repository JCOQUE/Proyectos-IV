from odoo import models, api
from kafka import KafkaConsumer
import logging
import threading

loggerC = logging.getLogger(__name__)

class KafkaConsumerSaleOrder(models.TransientModel):
    _name = 'kafka.consumer.sale.order'

    @api.model
    def consume_messages(self):
        try:
            # Configuración del consumidor
            kafka_server = '172.26.0.4:29093'
            topic_name = 'P00005'

            # Creación del consumidor
            PEDIDOS = KafkaConsumer(
                topic_name,
                bootstrap_servers=kafka_server,
                auto_offset_reset='earliest',  # Comienza desde el principio del tópico
                enable_auto_commit=True,  # Confirmaciones automáticas
            )

            # Escuchando mensajes
            for PEDIDO in PEDIDOS:
                loggerC.critical(f"Mensaje recibido CONSUMER: {PEDIDO.value.decode('utf-8')}")
                pedido = PEDIDO.value.decode('utf-8')
                nuevo_pedido = self.env['sale.order'].create({'name': 'PRUEBA'})
                nuevo_pedido = self.env['sale.order'].create([{'name': 'PRUEBA2'}])
                nuevo_pedido = self.env['sale.order'].create({'Number': 'PRUEBA3'})
                nuevo_pedido = self.env['sale.order'].create([{'Number': 'PRUEBA4'}])
                # Aquí puedes añadir tu lógica para manejar el mensaje y luego insertarlo en sale.order
            # No olvides cerrar el consumidor cuando termines
            PEDIDOS.close()
        except Exception as e: 
            loggerC.error(f"Error en el consumidor: {e}")
        

    def start_consumer_thread(self):
        threaded_calculation = threading.Thread(target=self.consume_messages)
        threaded_calculation.daemon = True
        threaded_calculation.start()

    def init(self):
        super(KafkaConsumerSaleOrder, self).init()
        self.start_consumer_thread()