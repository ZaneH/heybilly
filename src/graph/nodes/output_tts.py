from src.graph.action_node import ActionNode
from src.third_party.streamlabs import StreamlabsTTS, StreamlabsVoice
from src.voice.personality import Personality


class OutputTTSNode(ActionNode):
    create_queue = True  # Initially will be used for the Discord bot
    needs_uuid = True

    async def execute(self, input_data=None):
        personality = Personality()
        print(self.graph_processor.to_json(with_uuid=True))
        # print(self.graph_processor.pretty_print())
        # output = personality.suggest_edits(self.graph_processor.graph)
        # print(output)

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
