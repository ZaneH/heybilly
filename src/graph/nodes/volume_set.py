from src.graph.action_node import ActionNode


class VolumeSetNode(ActionNode):
    create_queue = True  # Initially will be used for the Discord bot

    async def execute(self, input_data=None):
        pass

    def validate_inputs(self) -> bool:
        """
        Validate that value was provided in the data field
        """
        if 'value' not in self.data:
            return False

        return True
