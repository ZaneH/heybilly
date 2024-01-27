import pika


class RabbitClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='actions_queue')

    def send_action(self, action: str):
        self.channel.basic_publish(
            exchange='', routing_key='actions_queue', body=action)
