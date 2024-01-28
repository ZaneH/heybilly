import asyncio

from dotenv import load_dotenv
load_dotenv()


async def main():
    from src.graph.builder import node_type_mapping
    from src.queue.rabbit_client import RabbitClient
    from src.voice.listen import Listen

    rabbit_client = RabbitClient()

    # Create a queue for the node if needed. Useful for your own integrations.
    def create_queues():
        for node_type in node_type_mapping:
            create_queue = node_type_mapping[node_type].create_queue

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
