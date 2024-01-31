import asyncio
import json
import logging

from tenacity import before_sleep_log, retry, stop_after_attempt, wait_fixed
from src.graph.builder import GraphBuilder
from src.voice.personality import Personality


logging.basicConfig()
log = logging.getLogger("tenacity.retry")
log.setLevel(logging.INFO)

retry_strategy = retry(
    wait=wait_fixed(2),  # Wait 2 seconds between retries
    stop=stop_after_attempt(3),  # Stop after 3 attempts
    before_sleep=before_sleep_log(log, logging.INFO)  # Log before retrying
)


class GraphProcessor:
    def __init__(self, rabbit_client, graph_data):
        self.graph = {}
        self.has_stale_text = False
        self.personality = Personality()
        self.rabbit_client = rabbit_client

        self.graph = GraphBuilder._create_nodes_from_json(graph_data, self)

        self.active_branches = 0
        self.executed_nodes = set()
        self.lock = asyncio.Lock()

    def on_graph_complete(self):
        logging.info("✅ Graph completed.")

    async def start(self):
        try:
            await self.graph["1"].process()
        except Exception as e:
            logging.error(f"Error processing graph: {e}")
            logging.error(self.graph)
            raise e

    @retry_strategy
    def add_personality(self):
        """
        Add personality to the graph. `has_stale_text` is set to True
        when the graph is updated with valuable information.
        """
        if self.has_stale_text == False:
            return

        personality_input = self.to_json(with_uuid=True)

        output = self.personality.suggest_edits(personality_input)
        self.apply_edits_to_graph(output)

        self.rabbit_client.log_ai_response(
            "ai.personality.responses", json.dumps({
                "input": json.loads(personality_input),
                "output": json.loads(output)
            }, indent=4)
        )

    def apply_edits_to_graph(self, edits_str):
        """
        Update the text in the graph based on the given edits.
        """
        try:
            # Load the edits object from the given string
            # (strict=False allows for more lenient parsing)
            edits_obj = json.loads(edits_str, strict=False)

            # Iterate through each edit in the 'edits' list
            for edit in edits_obj['edits']:
                # Extract node_uuid and the new text from the current edit
                node_uuid = edit['node_uuid']
                new_text = edit['text']

                # Find the node by its UUID
                node = self.find_node_by_uuid(node_uuid)

                # If the node is found, update its text
                if node:
                    logging.debug(
                        f"Updating node {node_uuid} with text: {new_text}")
                    node.data['text'] = new_text
                else:
                    logging.warning(f"No node found with UUID: {node_uuid}")

            self.has_stale_text = False

        except Exception as e:
            logging.warning(f"Couldn't update node text: {e}")
            logging.warning(f"Edits string: {edits_str}")
            raise e

    async def start_node(self, node) -> bool:
        """
        Start the given node if it hasn't already been executed.

        :param node: The node to start.
        :return: True if the node was started, False if it was already executed.
        """
        async with self.lock:
            if node.node_uuid not in self.executed_nodes:
                self.active_branches += 1
                self.executed_nodes.add(node.node_uuid)

                return True
            else:
                logging.debug(f"Node {node.node_uuid} was already executed.")
                return False

    async def finish_node(self, node):
        async with self.lock:
            if node.node_uuid in self.executed_nodes:
                self.active_branches -= 1

                if self.active_branches == 0:
                    self.on_graph_complete()

    async def wait_for_completion(self):
        while self.active_branches > 0:
            await asyncio.sleep(0.1)

        logging.debug("All branches have completed.")

    def to_json(self, with_uuid=False):
        # Serialize the entire graph to JSON
        graph_dict = {node_id: node.to_json(with_uuid=with_uuid)
                      for node_id, node in self.graph.items()}
        # Pretty print the JSON
        return json.dumps({"nodes": graph_dict}, indent=4)

    def pretty_print(self):
        logging.info("Graph:")
        for node in self.graph.values():
            logging.info(f"    {node}")

    def find_node_by_uuid(self, node_uuid):
        for node in self.graph.values():
            if node.node_uuid == node_uuid:
                return node
        return None
