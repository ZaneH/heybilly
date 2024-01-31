from src.graph.action_node import NodeIODataType

from src.graph.node_map import NODE_MAP


class NodeTypeValidationError(Exception):
    """Exception raised for errors in validating node types."""

    def __init__(self, message="Error validating node type"):
        self.message = message
        super().__init__(self.message)


class NodeIOValidationError(Exception):
    """Exception raised for errors in validating node connections."""

    def __init__(self, message="Error validating node connections"):
        self.message = message
        super().__init__(self.message)


class GraphValidator:
    @staticmethod
    def validate_nodes(data):
        nodes = data.get("nodes")
        if not nodes:
            raise ValueError("No nodes provided")

        for node_id, node_info in nodes.items():
            node_type = node_info["type"]
            if node_type not in NODE_MAP:
                raise NodeTypeValidationError(
                    f"Node type {node_type} is not valid")

    @staticmethod
    def validate_node_io(nodes):
        for node_id, node in nodes.items():
            for output_node in node.outputs:
                output_node_id = output_node.node_id

                if not output_node:
                    raise NodeIOValidationError(
                        f"Node {node_id} outputs to non-existent node {output_node}")

                # Check if output data type of the current node is compatible with the input data type of the output node
                if not GraphValidator.is_data_type_compatible(node.output_data_type, output_node.input_data_type):
                    raise NodeIOValidationError(
                        f"Node {node_id} outputs to node {output_node_id} with incompatible data types")

        return True

    @staticmethod
    def is_data_type_compatible(output_data_types, input_data_types):
        return bool(output_data_types & input_data_types) or NodeIODataType.NONE in output_data_types or NodeIODataType.NONE in input_data_types
