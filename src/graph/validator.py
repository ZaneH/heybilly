from src.graph.action_node import DataTypes

from src.graph.node_map import NODE_MAP


class NodeValidationError(Exception):
    """Exception raised for errors in validating node connections."""

    def __init__(self, message="Error validating node connections"):
        self.message = message
        super().__init__(self.message)


class GraphValidator:
    @staticmethod
    def validate_nodes(data):
        nodes = data.get("nodes")
        if not nodes:
            raise ValueError("No nodes to validate.")

        for node_id, node_info in nodes.items():
            node_type = node_info["type"]
            if node_type not in NODE_MAP:
                raise ValueError(f"Unknown node type: {node_type}")

    @staticmethod
    def validate_node_io(nodes):
        for node_id, node in nodes.items():
            for output_node_id in node.outputs:
                output_node = nodes.get(output_node_id.node_id)
                if not output_node:
                    raise NodeValidationError(
                        f"Node {node_id} outputs to non-existent node {output_node_id}")

                # Check if output data type of the current node is compatible with the input data type of the output node
                if not GraphValidator.is_data_type_compatible(node.output_data_type, output_node.input_data_type):
                    raise NodeValidationError(
                        f"Node {node_id} outputs to node {output_node_id} with incompatible data types")

        return True

    @staticmethod
    def is_data_type_compatible(output_data_type, input_data_type):
        # For now, this is a simple equality check
        is_none_type = output_data_type == DataTypes.NONE or input_data_type == DataTypes.NONE
        is_matching_type = output_data_type == input_data_type
        return is_none_type or is_matching_type
