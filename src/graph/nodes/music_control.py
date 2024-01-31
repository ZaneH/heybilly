from src.graph.action_node import ActionNode, DataTypes


class MusicControlNode(ActionNode):
    create_queue = False

    input_data_type = {DataTypes.NONE}
    output_data_type = {DataTypes.NONE}

    async def execute(self, input_data=None):
        self.send_node_to_queue()

    def validate_inputs(self) -> bool:
        return True
