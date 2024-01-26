from src.graph.action_node import ActionNode


class InputVoiceNode(ActionNode):
    def execute(self):
        # Logic to capture and transcribe voice input
        print("Processing voice input...")
