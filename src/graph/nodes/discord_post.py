from src.graph.action_node import ActionNode, NodeIODataType


class DiscordPostNode(ActionNode):
    create_queue = True
    can_add_personality = True

    # None = Any data type is accepted
    input_data_type = {NodeIODataType.NONE}
    output_data_type = {NodeIODataType.NONE}

    async def execute(self, input_data=None):
        new_text = ""
        if 'text' in self.data:
            new_text = self.data['text']

        # If no text was provided in the data field, use the input data
        # very important for continuity. There's needs to be a better way.
        # TODO: Figure out how validate_inputs plays into this
        if new_text == "" and type(input_data) == str:
            new_text = input_data

        # Update the text in the graph before adding personality
        self.data['text'] = new_text

        self.graph_processor.add_personality()

        self.send_node_to_queue()

    def validate_inputs(self) -> bool:
        """
        Validate that text was provided in the data field
        """
        if 'text' not in self.data:
            return False

        return True
