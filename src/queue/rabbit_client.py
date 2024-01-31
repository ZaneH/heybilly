import json
import pika


class RabbitClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                heartbeat=600,
                blocked_connection_timeout=300
            ))

        self.channel = self.connection.channel()

    def send_node(self, node_type: str, data: str):
        self.channel.basic_publish(
            exchange='', routing_key=node_type, body=data)

    def create_queue(self, queue_name: str, **kwargs):
        self.channel.queue_declare(queue=queue_name, **kwargs)

    def log_ai_response(self, queue_name: str, data: str):
        self.channel.basic_publish(
            exchange='', routing_key=queue_name, body=data)

    def send_status_update(self, status: str):
        self.channel.basic_publish(
            exchange='', routing_key='request.status', body=json.dumps({
                "status": status
            })
        )
