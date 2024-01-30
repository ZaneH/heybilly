from src.graph.action_node import ActionNode
from src.third_party.streamlabs import StreamlabsTTS, StreamlabsVoice
from src.third_party.streamelements import StreamElementsTTS
from src.utils.audio_player import LocalAudioPlayer
from src.utils.config import CLIArgs


class OutputTTSNode(ActionNode):
    create_queue = True  # Initially will be used for the Discord bot
    can_add_personality = True

    async def execute(self, input_data=None):
        self.graph_processor.add_personality()

        # Expecting this field to exist already
        text = self.data['text']

        if not text:
            raise Exception("No text provided to speak, retry.")

        tts_url = StreamElementsTTS(StreamlabsVoice.Justin).get_url(text)
        self.data['tts_url'] = tts_url

        if CLIArgs.use_discord_tts:
            self.send_node_to_queue()
        else:
            player = LocalAudioPlayer()
            player.play_stream(tts_url)

        return text

    def validate_inputs(self) -> bool:
        """
        Validate that text was provided in the data field
        """
        if 'text' not in self.data:
            return False

        return True
