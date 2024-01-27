from src.graph.action_node import ActionNode


class VolumeDownNode(ActionNode):
    create_queue = True

    async def execute(self, input_data=None):
        print(f"{self.node_type} ran")

        return True

    def validate_inputs(self) -> bool:
        return True
