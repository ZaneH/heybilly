import json
from tenacity import retry, wait_fixed, stop_after_attempt, before_sleep_log
import logging

logging.basicConfig()
log = logging.getLogger("tenacity.retry")
log.setLevel(logging.INFO)

retry_strategy = retry(
    wait=wait_fixed(2),  # Wait 2 seconds between retries
    stop=stop_after_attempt(3),  # Stop after 3 attempts
    before_sleep=before_sleep_log(log, logging.INFO)  # Log before retrying
)


async def retry_handler(func, *args, **kwargs):
    """
    Retry handler that applies the retry strategy to the provided function.
    """
    retrying_func = retry_strategy(func)
    return await retrying_func(*args, **kwargs)


class ActionNode:
    """
    Base class for all nodes that perform an action.

    Attributes:
    - node_id: The ID of the node
    - node_type: The type of the node
    - inputs: The input nodes
    - outputs: The output nodes
    - data: The data associated with the node
    - is_blocking: Whether the node is blocking
    """
    create_queue = True  # Should a RabbitMQ queue be created for this node?

    def __init__(self, node_id, node_type, inputs=[], outputs=[]):
        self.node_id = node_id
        self.node_type = node_type
        self.inputs = inputs
        self.outputs = outputs
        self.data = {}
        self.is_blocking = False
        self.rabbit_client = None

    async def execute(self):
        # Generic execution method, to be overridden by subclasses
        pass

    async def process(self):
        # Execute the current node and recursively process the next nodes
        await retry_handler(self.execute)
        for next_node in self.outputs:
            inputs_ok = next_node.validate_inputs()
            await next_node.process()

    def send_node_to_queue(self):
        if not self.rabbit_client:
            print("RabbitMQ client not set. Cannot send node to queue.")
            return

        self.rabbit_client.send_node(
            self.node_type, json.dumps(self.to_dict()))

    def validate_inputs(self) -> bool:
        # Generic validation method, to be overridden by subclasses
        return False

    def __str__(self):
        added_info = ""
        if self.data:
            added_info = f", Data={self.data}"
        if self.is_blocking:
            added_info += ", Blocking: ✅"

        inputs_satisfied = self.validate_inputs()
        if inputs_satisfied:
            added_info += ", Inputs: ✅"
        else:
            added_info += ", Inputs: ❌"

        return f"{type(self).__name__}(ID={self.node_id}, Type={self.node_type}, Outputs={self._output_ids()}{added_info})"

    def __repr__(self):
        return self.__str__()

    def _output_ids(self):
        # Helper method to get the IDs of the output nodes
        return [node.node_id for node in self.outputs]

    def to_dict(self):
        # Convert all attributes to a dictionary
        node_dict = self.__dict__.copy()

        # Replace output nodes with their IDs in the dictionary
        node_dict['outputs'] = self._output_ids()

        return node_dict
