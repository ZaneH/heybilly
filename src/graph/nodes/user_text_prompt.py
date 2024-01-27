
from src.graph.action_node import ActionNode


class UserTextPromptNode(ActionNode):
    create_queue = False
    is_blocking = True

    async def execute(self, input_data=None):
        pass

    def validate_inputs(self) -> bool:
        """
        Validate that text was provided in the data field
        """
        if 'text' not in self.data:
            return False

        return True
