import asyncio
import logging
import argparse

from dotenv import load_dotenv
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument(
    '--verbose', help='Enable verbose logging', action='store_true')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(name)s: %(message)s')

else:
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.basicConfig(level=logging.INFO,
                        format='%(name)s: %(message)s')


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
        args = {'x-max-length': 10}
        rabbit_client.create_queue("ai.builder.responses", arguments=args)
        rabbit_client.create_queue("ai.personality.responses", arguments=args)

    create_queues()

    listener = Listen(rabbit_client)
    await listener.start()


if __name__ == "__main__":
    asyncio.run(main())
