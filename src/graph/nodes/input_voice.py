from src.graph.action_node import ActionNode, DataTypes


class InputVoiceNode(ActionNode):
    create_queue = False

    output_data_type = {DataTypes.STRING}

    async def execute(self, input_data=None):
        return getattr(self.data, 'text', None)

    def validate_inputs(self) -> bool:
        """
        Validate that text was provided in the data field
        """
        if 'text' not in self.data:
            return False

        return True
