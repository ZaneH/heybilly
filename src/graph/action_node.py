import asyncio
import json
from tenacity import retry, wait_fixed, stop_after_attempt, before_sleep_log
import logging

from src.utils.random import random_id

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


async def retry_handler(func, *args, **kwargs):
    """
    Retry handler that applies the retry strategy to the provided function.
    """
    retrying_func = retry_strategy(func)
    return await retrying_func(*args, **kwargs)


def log_custom_message(retry_state):
    attempt_number = retry_state.attempt_number
    log.debug(
        f"Attempt {attempt_number}: Retrying node in {retry_state.next_action.sleep} seconds")


def handle_retry_error(retry_state):
    log.error(
        f"Error prcessing node after {retry_state.attempt_number} attempts")
    log.error(retry_state.outcome.exception())
    return retry_state.outcome.result()


retry_strategy = retry(
    wait=wait_fixed(2),
    stop=stop_after_attempt(3),
    before_sleep=log_custom_message,
    retry_error_callback=handle_retry_error
)


class ActionNode:
    """
    Base class for all nodes that perform an action.

    Attributes:
    - node_id: The ID of the node
    - node_type: The type of the node
    - inputs: (Unused) The input nodes
    - outputs: The output nodes
    - data: The data associated with the node
    - is_blocking: (Unused) Whether the node is blocking
    """
    create_queue = True  # Should a RabbitMQ queue be created for this node?
    can_add_personality = False  # Should personality ever be added to this node?

    def __init__(self, node_id, node_type, inputs=[], outputs=[]):
        self.node_id = node_id
        self.node_type = node_type
        self.inputs = inputs
        self.outputs = outputs
        self.data = {}
        self.is_blocking = False
        self.node_uuid = random_id()

    async def execute(self, input_data=None):
        # Generic execution method, to be overridden by subclasses
        return None

    async def process(self, input_data=None):
        should_execute = await self.graph_processor.start_node(self)
        if not should_execute:
            return

        async def execute_wrapper():
            if input_data is None:
                logging.info(f"- Running {self.node_type}.")
            else:
                logging.info(
                    f"- Running {self.node_type} with input data.")
                logging.info(f"{self}")

            return await self.execute(input_data)

        try:
            # Execute the current node and recursively process the next nodes
            output_data = await retry_handler(execute_wrapper)
        except Exception as e:
            logging.error(f"Final error after retries: {e}")
            raise e

        tasks = []
        for next_node in self.outputs:
            tasks.append(next_node.process(output_data))
        if tasks:
            await asyncio.gather(*tasks)

        await self.graph_processor.finish_node(self)

    def send_node_to_queue(self):
        if not hasattr(self.graph_processor, "rabbit_client"):
            logging.critical(
                "RabbitMQ client not set. Cannot send node to queue.")
            return

        rc = self.graph_processor.rabbit_client

        logging.debug(f"Sending node to queue: {str(self)}")
        rc.send_node(self.node_type, json.dumps(self.to_dict()))

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

    # Being used for OpenAI serialization
    def to_json(self, with_uuid=False):
        # Convert the node to a JSON-serializable dictionary
        object = {
            'node_id': self.node_id,
            'node_type': self.node_type,
        }

        inputs = [node.node_id for node in self.inputs]
        outputs = [node.node_id for node in self.outputs]
        data = self.data

        if inputs:
            object['inputs'] = inputs

        if outputs:
            object['outputs'] = outputs

        if data:
            object['data'] = data

        if with_uuid and self.can_add_personality:
            object['node_uuid'] = self.node_uuid

        return object

    # Being used for RabbitMQ serialization
    def to_dict(self):
        # Convert all attributes to a dictionary
        node_dict = self.__dict__.copy()

        # Drop the graph processor attribute
        node_dict.pop('graph_processor', None)

        # Drop input/output nodes
        node_dict.pop('inputs', None)
        node_dict.pop('outputs', None)

        return node_dict
