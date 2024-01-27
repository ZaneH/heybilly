from src.graph.action_node import ActionNode


class YouTubePlayNode(ActionNode):
    create_queue = True

    async def execute(self, input_data=None):
        pass

        return True

    def validate_inputs(self) -> bool:
        return True
