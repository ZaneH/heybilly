import asyncio
import logging

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format='%(name)s: %(message)s')

# Adjust 'httpx' with the name of the library
logging.getLogger('httpx').setLevel(logging.WARNING)


async def main():
    from src.graph.builder import NODE_MAP
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
