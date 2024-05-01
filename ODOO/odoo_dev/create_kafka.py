import sys
import yaml
import re
import socket



def save_file(file):
    try:
        print('Guardando YAML...')
        with open("kafka.yaml", "w") as f:
            f.write(file)
        print('YAML guardado como kafka.yaml')
    except:
        print('Hubo un problema al guardar el YAML')
        sys.exit()


def create_yaml(local_ip):
    data = [
        {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": "kafka-service"
            },
            "spec": {
                "selector": {
                    "app": "kafka"
                },
                "ports": [
                    {
                        "protocol": "TCP",
                        "port": 9092,
                        "targetPort": 9092,
                        "nodePort": 31234
                    }
                ],
                "type": "NodePort"
            }
        },
        {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": "kafka-deployment",
                "labels": {
                    "app": "kafka"
                }
            },
            "spec": {
                "replicas": 1,
                "selector": {
                    "matchLabels": {
                        "app": "kafka"
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": "kafka"
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": "broker",
                                "image": "confluentinc/cp-kafka:7.0.1",
                                "ports": [
                                    {
                                        "containerPort": 9092
                                    }
                                ],
                                "env": [
                                    {
                                        "name": "KAFKA_ZOOKEEPER_CONNECT",
                                        "value": "zookeeper-service:2181"
                                    },
                                    {
                                        "name": "KAFKA_LISTENERS",
                                        "value": "PLAINTEXT_INTERNAL://0.0.0.0:9092"
                                    },
                                    {
                                        "name": "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP",
                                        "value": "PLAINTEXT_INTERNAL:PLAINTEXT"
                                    },
                                    {
                                        "name": "KAFKA_ADVERTISED_LISTENERS",
                                        "value": f"PLAINTEXT_INTERNAL://{local_ip}:31234"
                                    },
                                    {
                                        "name": "KAFKA_INTER_BROKER_LISTENER_NAME",
                                        "value": "PLAINTEXT_INTERNAL"
                                    },
                                    {
                                        "name": "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR",
                                        "value": "1"
                                    },
                                    {
                                        "name": "KAFKA_TRANSACTION_STATE_LOG_MIN_ISR",
                                        "value": "1"
                                    },
                                    {
                                        "name": "KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR",
                                        "value": "1"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
    ]

    try:
        yaml_data = yaml.dump_all(data, default_flow_style=False)
    except:
        print('Algo salió mal al pasar de formato JSON a YAML')

    save_file(yaml_data)

if __name__ == "__main__":
    # if len(sys.argv) == 2:
        #is_valid_ipv4(sys.argv[1])
    print("Creando YAML...")
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(local_ip)
    create_yaml(local_ip)


