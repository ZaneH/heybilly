from src.graph.action_node import ActionNode


class YouTubePlayNode(ActionNode):
    create_queue = True

    async def execute(self, input_data=None):
        if type(input_data) != str:
            raise Exception("Input data must be a string")

        self.data['video_url'] = input_data

        self.send_node_to_queue()

        return True

    def validate_inputs(self) -> bool:
        return True
