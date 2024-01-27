
from src.graph.action_node import ActionNode


class UserTextPromptNode(ActionNode):
    is_blocking = True

    async def execute(self):
        print(f"{self.node_type} ran")

    def validate_inputs(self) -> bool:
        """
        Validate that text was provided in the data field
        """
        if 'text' not in self.data:
            return False

        return True
