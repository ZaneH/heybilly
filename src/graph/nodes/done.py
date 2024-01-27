from src.graph.action_node import ActionNode


class DoneNode(ActionNode):
    create_queue = False

    async def execute(self, input_data=None):
        return True

    def validate_inputs(self) -> bool:
        return True
