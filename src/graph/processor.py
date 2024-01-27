import json
from src.graph.builder import GraphBuilder


class GraphProcessor:
    def __init__(self, rabbit_client, graph_data):
        self.graph = {}
        self.current_node = "1"
        self.rabbit_client = rabbit_client
        self.create_graph(graph_data)

    def create_graph(self, graph_data):
        nodes = GraphBuilder._create_nodes_from_json(graph_data, self)
        self.graph = nodes

    def to_json(self, with_uuid=False):
        # Serialize the entire graph to JSON
        graph_dict = {node_id: node.to_json(with_uuid=with_uuid)
                      for node_id, node in self.graph.items()}
        return json.dumps(graph_dict, indent=4)  # Pretty print the JSON

    def pretty_print(self):
        print("Graph:")
        for node in self.graph.values():
            print("    ", node)

    async def start(self):
        try:
            await self.graph[self.current_node].process()
        except Exception as e:
            print("Error processing graph:", e)
            print(self.pretty_print())
