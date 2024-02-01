import json
import pika
import asyncio


class RabbitClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                heartbeat=600,
                blocked_connection_timeout=300
            ))

        loop = asyncio.get_event_loop()
        self._pde_heartbeat = loop.create_task(
            self.process_data_events_heartbeat())

        self.channel = self.connection.channel()

    def close(self):
        self._pde_heartbeat.cancel()

    async def process_data_events_heartbeat(self):
        while True:
            self.connection.process_data_events()
            await asyncio.sleep(60)

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
