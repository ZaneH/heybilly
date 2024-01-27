from src.graph.action_node import ActionNode


class GiphySearchNode(ActionNode):
    create_queue = False

    async def execute(self, input_data=None):
        pass

    def validate_inputs(self) -> bool:
        """
        Validate that query was provided in the data field
        """
        if 'query' not in self.data:
            return False

        return True
