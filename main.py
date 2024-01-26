import json
from dotenv import load_dotenv
load_dotenv()


def main():
    from src.graph.builder import GraphBuilder
    builder = GraphBuilder()
    graph = builder.build_graph(
        "Hey Billy, turn the volume up and post a car meme to Discord.")
    print(graph)


if __name__ == "__main__":
    main()
