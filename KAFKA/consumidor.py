from kafka import KafkaConsumer
import json
# Crear una instancia del consumidor de Kafka
consumer = KafkaConsumer(
    'tema-prueba-ERP',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,  # Desactivar el commit automático
    group_id='my-group',
    value_deserializer=lambda x: x.decode('utf-8'))

# Leer, mostrar y cometer mensajes manualmente
for message in consumer:
    dic = json.loads(message.value)
    
    print(f"Recibido: {dic}")  
    print(f"Recibido: {dic['entero']}")  
    print(f"Recibido: {dic['string']}")  
    # Cometer el offset del mensaje procesado
    # consumer.commit() #? Una vez leidos ocultamos los mensajes
