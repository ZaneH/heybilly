from src.graph.action_node import ActionNode
from src.third_party.streamlabs import StreamlabsTTS, StreamlabsVoice


class OutputTTSNode(ActionNode):
    create_queue = True  # Initially will be used for the Discord bot

    async def execute(self):
        text = getattr(self.data, 'text', None)
        if not text:
            raise Exception("No text provided to speak, retry.")

        tts_url = StreamlabsTTS(StreamlabsVoice.Justin).get_url(text)
        setattr(self.data, 'tts_url', tts_url)

        print("Speaking", text)
        self.send_node_to_queue()

    def validate_inputs(self) -> bool:
        """
        Validate that text was provided in the data field
        """
        if 'text' not in self.data:
            return False

        return True
