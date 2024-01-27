class ActionNode:
    def __init__(self, node_id, node_type, inputs=[], outputs=[]):
        self.node_id = node_id
        self.node_type = node_type
        self.inputs = inputs
        self.outputs = outputs
        self.data = {}
        self.is_blocking = False

    async def execute(self):
        # Generic execution method, to be overridden by subclasses
        pass

    async def process(self):
        # Execute the current node and recursively process the next nodes
        await self.execute()
        for next_node in self.outputs:
            inputs_ok = next_node.validate_inputs()
            await next_node.process()

    def validate_inputs(self) -> bool:
        # Generic validation method, to be overridden by subclasses
        return False

    def __str__(self):
        added_info = ""
        if self.data:
            added_info = f", Data={self.data}"
        if self.is_blocking:
            added_info += ", Blocking: ✅"

        inputs_satisfied = self.validate_inputs()
        if inputs_satisfied:
            added_info += ", Inputs: ✅"
        else:
            added_info += ", Inputs: ❌"

        return f"{type(self).__name__}(ID={self.node_id}, Type={self.node_type}, Outputs={self._output_ids()}{added_info})"

    def __repr__(self):
        return self.__str__()

    def _output_ids(self):
        # Helper method to get the IDs of the output nodes
        return [node.node_id for node in self.outputs]

    def to_dict(self):
        # Convert all attributes to a dictionary
        node_dict = self.__dict__.copy()

        # Replace output nodes with their IDs in the dictionary
        node_dict['outputs'] = self._output_ids()

        return node_dict
