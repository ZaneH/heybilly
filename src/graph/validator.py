from src.graph.builder import NODE_MAP


class GraphValidator:
    """
    Will come back to this later.
    Graphs are valid if:

    1. All types match the node_type_mapping.
    2. There is an "input.voice" to start
    3. There is a "done" node to end.
    """
    @staticmethod
    def validate_nodes(data):
        for node_id, node_info in data["nodes"].items():
            node_type = node_info["type"]
            if node_type not in NODE_MAP:
                raise ValueError(f"Unknown node type: {node_type}")
