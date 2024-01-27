from src.graph.action_node import ActionNode


class WolframSimpleNode(ActionNode):
    create_queue = False

    async def execute(self):
        print(f"{self.node_type} ran")

    def validate_inputs(self) -> bool:
        """
        Validate that query was provided in the data field
        """
        if 'query' not in self.data:
            return False

        return True
