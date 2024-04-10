from kafka import KafkaConsumer
import json
import logging
from concurrent.futures import ThreadPoolExecutor
import threading

# Configuración del consumidor
kafka_server = '172.26.0.4:29093'
topic_name = 'P00005'

_logger = logging.getLogger(__name__)

def consume_messages():
    try:
        # Creación del consumidor
        consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=kafka_server,
            auto_offset_reset='earliest',  # Comienza desde el principio del tópico
            enable_auto_commit=True,  # Confirmaciones automáticas
            value_deserializer=lambda x: x.decode('utf-8')  # Deserializador para los mensajes
        )

        # Escuchando mensajes
        for message in consumer:
            print(f"Mensaje recibido: {message.value.decode('utf-8')}")
            _logger.info(f"Mensaje recibido: {message.value.decode('utf-8')}")
            # Aquí puedes añadir tu lógica para manejar el mensaje

        # No olvides cerrar el consumidor cuando termines
        consumer.close()
    except Exception as e: 
        _logger.error(f"Error en el consumidor: {e}")

threaded_calculation = threading.Thread(
                target= consume_messages,)
threaded_calculation.start()
