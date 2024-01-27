import json
from dotenv import load_dotenv
load_dotenv()


def main():
    from src.graph.builder import GraphBuilder
    from src.queue.rabbit_client import RabbitClient

    rabbit_queue = RabbitClient()
    builder = GraphBuilder()
    graph = builder.build_graph(
        "Hey Billy, turn the volume up and post a car meme to Discord.")
    print(graph)
    rabbit_queue.send_action(json.dumps(graph["1"].to_dict()))


if __name__ == "__main__":
    main()
