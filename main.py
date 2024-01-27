import asyncio

from dotenv import load_dotenv
load_dotenv()


async def main():
    from src.graph.builder import GraphBuilder, node_type_mapping
    from src.graph.processor import GraphProcessor
    from src.queue.rabbit_client import RabbitClient
    from src.voice.listen import Listen

    rabbit_client = RabbitClient()

    # Create a queue for each node. Useful for your own integrations.
    def create_queues():
        for node_type in node_type_mapping:
            create_queue = node_type_mapping[node_type].create_queue
            if create_queue:
                rabbit_client.create_queue(node_type)

    create_queues()

    builder = GraphBuilder(rabbit_client)
    graph = builder.build_graph(
        "Yo Billy, tell me what the price of gold is.")
    processor = GraphProcessor(graph)
    await processor.start()

    listener = Listen()
    await listener.start()


if __name__ == "__main__":
    asyncio.run(main())
