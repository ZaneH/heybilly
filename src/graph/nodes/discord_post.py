from src.graph.action_node import ActionNode


class DiscordPostNode(ActionNode):
    create_queue = True  # Initially will be used for the Discord bot
    needs_uuid = True

    async def execute(self, input_data=None):
        # Update the text in the graph before adding personality
        new_text = ""
        if type(input_data) == str:
            new_text += input_data

        if getattr(self.data, 'text', None):
            new_text += self.data['text']

        # TODO: Figure out how validate_inputs plays into this
        if type(new_text) != str:
            raise Exception("Input data must be a string")

        self.data['text'] = new_text

        self.graph_processor.add_personality()

        self.send_node_to_queue()

        return True

    def validate_inputs(self) -> bool:
        """
        Validate that text was provided in the data field
        """
        if 'text' not in self.data:
            return False

        return True
