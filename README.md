## Intro

Este trabajo consiste en realizar un protocolo de pedidos entre dos ERP, para compra-venta. Para este protocolo de pedidos, la herramienta que se ha utilizadoara la transmisión de mesajes ha sido KAFKA. Por otra parte, la herramienta que se ha utilizado para simular los ERP ha sido el ERP open-source de ODOO.

Estos ERP están desplegados con Docker, a través de la imagen de Odoo encontrada en DockerHub. Adicionmalmente, este despligue de esta aplicación está hecho con Kubernetes. De esta manera se consigue una aplicación tolerante a fallos y escalable. También, por otra parte, se han encriptado los mensajes que pasan por Kafka, añadiendo una capa de seguridad a nuestra aplicación.


Por otra parte, el Dashboard se ha realizado en código Javascript; concretamente con la librería ChartsJS. 


## Referencias
#### Dashboard
- https://www.youtube.com/watch?v=CJvaY-VGqwk&pp=ygUhZGFzaGJvYXJkIGluIE9kb28gd2l0aCBqYXZhc2NyaXB0
- https://www.youtube.com/watch?v=I8E9XszUYGY&pp=ygUhZGFzaGJvYXJkIGluIE9kb28gd2l0aCBqYXZhc2NyaXB0
