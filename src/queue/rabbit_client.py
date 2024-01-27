import pika


class RabbitClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

    def send_action(self, action: str):
        self.channel.basic_publish(
            exchange='', routing_key='actions_queue', body=action)

    def create_queue(self, queue_name: str):
        self.channel.queue_declare(queue=queue_name)
