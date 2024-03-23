from kafka import KafkaProducer

# Crear una instancia del productor de Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         max_block_ms=1048588,
                         compression_type='gzip')

# Enviar un mensaje al tópico 'tema-prueba-ERP'
producer.send('tema-prueba-ERP', b'{"entero":1,"string":"HOLA esto es una prueba5"}', partition=1 )

# Asegurarse de que todos los mensajes hayan sido enviados
producer.flush()

# Cerrar el productor
producer.close()
