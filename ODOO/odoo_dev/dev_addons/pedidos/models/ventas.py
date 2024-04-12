from odoo import models, api
from kafka import KafkaConsumer
import logging
import threading

_logger = logging.getLogger(__name__)

class KafkaConsumerSaleOrder(models.TransientModel):
    _name = 'kafka.consumer.sale.order'

    @api.model
    def consume_messages(self):
        try:
            # Configuración del consumidor
            kafka_server = '172.26.0.4:29093'
            topic_name = 'P00005'

            # Creación del consumidor
            consumer = KafkaConsumer(
                topic_name,
                bootstrap_servers=kafka_server,
                auto_offset_reset='earliest',  # Comienza desde el principio del tópico
                enable_auto_commit=True,  # Confirmaciones automáticas
            )

            # Escuchando mensajes
            for message in consumer:
                _logger.info(f"Mensaje recibido: {message.value.decode('utf-8')}")
                pedido = message.value.decode('utf-8')
                # Aquí puedes añadir tu lógica para manejar el mensaje y luego insertarlo en sale.order
            # No olvides cerrar el consumidor cuando termines
            consumer.close()
        except Exception as e: 
            _logger.error(f"Error en el consumidor: {e}")
        nuevo_pedido = self.env['sale.order'].create(pedido)

    def start_consumer_thread(self):
        threaded_calculation = threading.Thread(target=self.consume_messages)
        threaded_calculation.daemon = True
        threaded_calculation.start()

    def init(self):
        super(KafkaConsumerSaleOrder, self).init()
        self.start_consumer_thread()