from src.graph.action_node import ActionNode


class DiscordPostNode(ActionNode):
    create_queue = True  # Initially will be used for the Discord bot

    async def execute(self, input_data=None):
        self.send_node_to_queue()

        return True

    def validate_inputs(self) -> bool:
        """
        Validate that text was provided in the data field
        """
        if 'text' not in self.data:
            return False

        return True
