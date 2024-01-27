import asyncio
import json
from src.graph.builder import GraphBuilder


class GraphProcessor:
    def __init__(self, rabbit_client, graph_data):
        self.graph = {}
        self.current_node = "1"
        self.has_stale_text = False
        self.rabbit_client = rabbit_client

        self.graph = GraphBuilder._create_nodes_from_json(graph_data, self)

        self.active_branches = 0
        self.lock = asyncio.Lock()

    def on_graph_complete(self):
        print("✅ Graph completed.")

    def find_node_by_uuid(self, node_uuid):
        for node in self.graph.values():
            if node.node_uuid == node_uuid:
                return node
        return None

    def apply_edits_to_graph(self, edits_str):
        """
        Update the text in the graph based on the given edits.
        """
        if not self.has_stale_text:
            return

        try:
            # Load the edits object from the given string
            edits_obj = json.loads(edits_str)
            print("Loaded edits:", edits_obj)

            # Iterate through each edit in the 'edits' list
            for edit in edits_obj['edits']:
                # Extract node_uuid and the new text from the current edit
                node_uuid = edit['node_uuid']
                new_text = edit['text']

                # Find the node by its UUID
                node = self.find_node_by_uuid(node_uuid)

                # If the node is found, update its text
                if node:
                    node.data['text'] = new_text
                    print(f"Updated text for node {node_uuid}: {new_text}")
                else:
                    print(f"No node found with UUID: {node_uuid}")

            self.has_stale_text = False

        except Exception as e:
            print("Error updating node text:", e)
            print("Edits string:", edits_str)

    async def start_node(self, node):
        async with self.lock:
            self.active_branches += 1

    async def finish_node(self, node):
        async with self.lock:
            self.active_branches -= 1

            if self.active_branches == 0:
                self.on_graph_complete()

    async def wait_for_completion(self):
        while self.active_branches > 0:
            await asyncio.sleep(0.1)
        print("All branches have completed.")

    def to_json(self, with_uuid=False):
        # Serialize the entire graph to JSON
        graph_dict = {node_id: node.to_json(with_uuid=with_uuid)
                      for node_id, node in self.graph.items()}
        # Pretty print the JSON
        return json.dumps({"nodes": graph_dict}, indent=4)

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
