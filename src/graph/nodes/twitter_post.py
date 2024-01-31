from src.graph.action_node import ActionNode, NodeIODataType


class TwitterPostNode(ActionNode):
    create_queue = False

    input_data_type = {NodeIODataType.URL, NodeIODataType.STRING}

    async def execute(self, input_data=None):
        pass

    def validate_inputs(self) -> bool:
        """
        Validate that text was provided in the data field
        """
        if 'text' not in self.data:
            return False

        return True
