from src.graph.action_node import ActionNode


class InputVoiceNode(ActionNode):
    create_queue = False

    async def execute(self, input_data=None):
        print(f"{self.node_type} ran")

        return getattr(self.data, 'text', None)

    def validate_inputs(self) -> bool:
        """
        Validate that text was provided in the data field
        """
        if 'text' not in self.data:
            return False

        return True
