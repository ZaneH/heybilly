import argparse
import asyncio
import logging

from dotenv import load_dotenv

from src.utils.config import CLIArgs

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument(
    '--verbose', help='Enable verbose logging', action='store_true')
parser.add_argument(
    '--discord-tts', help='Play text-to-speech through Discord bot rather than computer audio', action='store_true')

args = parser.parse_args()


async def main():
    from src.graph.node_map import NODE_MAP
    from src.queue.rabbit_client import RabbitClient
    from src.voice.listen import Listen

    rabbit_client = RabbitClient()

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

    create_queues()

    listener = Listen(rabbit_client)
    await listener.start()


def load_config():
    CLIArgs.use_discord_tts = args.discord_tts


def configure_logging():
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    logging.getLogger('aio_pika').setLevel(logging.WARNING)
    logging.getLogger('pika').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('openai').setLevel(logging.WARNING)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(name)s: %(message)s')

    else:
        logging.basicConfig(level=logging.INFO,
                            format='%(name)s: %(message)s')


if __name__ == "__main__":
    load_config()
    configure_logging()

    asyncio.run(main())
