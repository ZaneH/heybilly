class ActionNode:
    def __init__(self, node_id, node_type, inputs=[], outputs=[]):
        self.node_id = node_id
        self.node_type = node_type
        self.inputs = inputs
        self.outputs = outputs

    def execute(self):
        # Generic execution method, to be overridden by subclasses
        pass

    def process(self):
        # Execute the current node and recursively process the next nodes
        self.execute()
        for next_node in self.outputs:
            next_node.process()

    def __str__(self):
        return f"ActionNode(ID={self.node_id}, Type={self.node_type}, Outputs={self._output_ids()})"

    def __repr__(self):
        return self.__str__()

    def _output_ids(self):
        # Helper method to get the IDs of the output nodes
        return [node.node_id for node in self.outputs]
