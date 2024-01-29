from src.graph.action_node import ActionNode


class SoundEffectNode(ActionNode):
    create_queue = True  # Initially will be used for the Discord bot

    async def execute(self, input_data=None):
        if type(input_data) != str:
            raise Exception(
                f"Input data must be a string. Got {type(input_data)}")

        self.data['video_url'] = input_data

        self.send_node_to_queue()

        return True

    def validate_inputs(self) -> bool:
        """
        Validate that video_id was provided in the data field
        """
        if 'video_id' not in self.data:
            return False

        return True
