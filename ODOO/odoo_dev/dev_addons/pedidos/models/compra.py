from odoo import models, fields, api
from kafka import KafkaProducer
import logging
import json
import base64
from kafka.admin import KafkaAdminClient, NewTopic


_logger = logging.getLogger(__name__)

class purchase_custom(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        _logger.info("HACIENDO PRUEBAS DE QUE HAY CAMBIOS 1")
        # Datos de configuración de Kafka
        kafka_server = "172.22.0.5:29093"  # Ajusta según tu configuración
        topic_name = self.name
        _logger.info(topic_name)

        # Crear el cliente de administración de Kafka
        admin_client = KafkaAdminClient(
            bootstrap_servers=kafka_server,
            client_id='admin'
        )
        _logger.info("HACIENDO PRUEBAS DE QUE HAY CAMBIOS 2")
        # Crear un objeto NewTopic
        topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)

        # Crear el tópico
        try:
            admin_client.create_topics(new_topics=[topic], validate_only=False)
        except Exception as e:
            _logger.error(f"Error al crear el tópico: {e}")

        # Crear una instancia del productor de Kafka
        producer = KafkaProducer(bootstrap_servers=kafka_server,
                                 max_block_ms=1048588,
                                 compression_type='gzip')
        log_data = {
            "Usuario": self.partner_id.name,
            "Pedido": self.name,
            "Referencia Proveedor": self.partner_ref,
            "Moneda": self.currency_id.name,
            "Fecha esperada": self.date_planned.strftime('%Y-%m-%d'),
            "Productos": []
        }

        # Loop through order lines and add product information to a list
        for product in self.order_line:
            product_info = {
                "Nombre": product.product_id.name,
                "Descripción": product.name,
                "Cantidad": product.product_qty,
                "Recibido": product.qty_received,
                "Facturado": product.qty_invoiced,
                "Precio Unitario": product.price_unit,
                "Impuestos": product.taxes_id.name,
                "Subtotal": product.price_subtotal
            }
            log_data["Productos"].append(product_info)

        # Convertir los datos a JSON y codificarlos en base64
        json_data = json.dumps(log_data)
        encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')

        # Enviar el mensaje al tópico de Kafka
        try:
            producer.send(topic_name, encoded_data.encode('utf-8'))
            producer.flush()
        except Exception as e:
            _logger.error(f"Error al enviar el mensaje a Kafka: {e}")
        finally:
            producer.close()

        _logger.info(log_data)
        _logger.info("HACIENDO PRUEBAS DE QUE HAY CAMBIOS 3")

        return True