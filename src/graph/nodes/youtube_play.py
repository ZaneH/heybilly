from src.graph.action_node import ActionNode, DataTypes


class YouTubePlayNode(ActionNode):
    create_queue = True

    input_data_type = {DataTypes.URL}
    output_data_type = {DataTypes.NONE}

    async def execute(self, input_data=None):
        if type(input_data) != str:
            raise Exception("Input data must be a string")

        self.data['video_url'] = input_data

        self.send_node_to_queue()

    def validate_inputs(self) -> bool:
        return True
