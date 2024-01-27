import asyncio
from dotenv import load_dotenv
load_dotenv()


async def main():
    from src.graph.builder import GraphBuilder, node_type_mapping
    from src.queue.rabbit_client import RabbitClient
    from src.graph.processor import GraphProcessor

    rabbit_queue = RabbitClient()

    def create_queues():
        # TODO: improve this system of queue creation
        no_queue_types = ['done', 'input.voice',
                          'giphy.search', 'twitter.post', 'user_text_prompt']
        for node_type in node_type_mapping:
            if node_type in no_queue_types:
                continue

            rabbit_queue.create_queue(node_type)

    create_queues()

    builder = GraphBuilder()
    graph = builder.build_graph(
        "Hey Billy, turn the volume up and post a car meme to Discord.")
    processor = GraphProcessor(graph)
    await processor.start()


if __name__ == "__main__":
    asyncio.run(main())
