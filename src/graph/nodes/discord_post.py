from src.graph.action_node import ActionNode


class DiscordPostNode(ActionNode):
    create_queue = True  # Initially will be used for the Discord bot
    can_add_personality = True

    async def execute(self, input_data=None):
        new_text = ""
        if 'text' in self.data:
            new_text = self.data['text']

        # If no text was provided in the data field, use the input data
        # very important for continuity. There's needs to be a better way.
        # TODO: Figure out how validate_inputs plays into this
        if new_text == "" and type(input_data) == str:
            new_text = input_data

        if type(new_text) != str:
            raise Exception("Input data must be a string")

        # Update the text in the graph before adding personality
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
