import asyncio
import logging

from dotenv import load_dotenv

from src.utils.commandline import CommandLine
from src.utils.config import CLIArgs

load_dotenv()


def main():
    from src.graph.node_map import NODE_MAP
    from src.queue.rabbit_client import RabbitClient
    from src.voice.listen import Listen

    try:
        rabbit_client = RabbitClient()
    except Exception as e:
        logging.error(
            "Error connecting to RabbitMQ. Use `make rabbitmq` to start a container.\nExiting...")
        logging.error(e)
        return

    # Create a queue for the node if needed. Useful for your own integrations.
    def create_queues():
        for node_type in NODE_MAP:
            create_queue = NODE_MAP[node_type].create_queue

            if create_queue:
                rabbit_client.create_queue(node_type)

        # Used for logging and easily fine-tuning the AI
        queue_args = {'x-max-length': 10}
        rabbit_client.create_queue(
            "ai.builder.responses", arguments=queue_args)
        rabbit_client.create_queue(
            "ai.personality.responses", arguments=queue_args)

        # Used to signal for thinking/idle
        rabbit_client.create_queue("request.status", arguments=queue_args)

    create_queues()

    def _on_interrupt():
        logging.info("Exiting...")
        rabbit_client.close()

    listener = Listen(rabbit_client)
    listener.on_interrupt_callback = _on_interrupt
    listener.start()


def load_config():
    args = CommandLine().read_command_line()
    CLIArgs.update_from_args(args)


def configure_logging():
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    logging.getLogger('aio_pika').setLevel(logging.WARNING)
    logging.getLogger('pika').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('openai').setLevel(logging.WARNING)
    logging.getLogger('faster_whisper').setLevel(logging.WARNING)

    if CLIArgs.verbose:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(name)s: %(message)s')

    else:
        logging.basicConfig(level=logging.INFO,
                            format='%(name)s: %(message)s')


if __name__ == "__main__":
    load_config()
    configure_logging()

    main()
