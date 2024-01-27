from src.graph.action_node import ActionNode


class DoneNode(ActionNode):
    create_queue = False

    async def execute(self):
        print(f"{self.node_type} ran")

    def validate_inputs(self) -> bool:
        return True
