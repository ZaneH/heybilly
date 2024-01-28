from src.graph.nodes.discord_post import DiscordPostNode
from src.graph.nodes.done import DoneNode
from src.graph.nodes.giphy_search import GiphySearchNode
from src.graph.nodes.input_voice import InputVoiceNode
from src.graph.nodes.output_tts import OutputTTSNode
from src.graph.nodes.sound_effect import SoundEffectNode
from src.graph.nodes.twitter_post import TwitterPostNode
from src.graph.nodes.user_text_prompt import UserTextPromptNode
from src.graph.nodes.volume_set import VolumeSetNode
from src.graph.nodes.wolfram_simple import WolframSimpleNode
from src.graph.nodes.youtube_play import YouTubePlayNode
from src.graph.nodes.youtube_search import YouTubeSearchNode

NODE_MAP = {
    "input.voice": InputVoiceNode,
    "user_text_prompt": UserTextPromptNode,
    "twitter.post": TwitterPostNode,
    "discord.post": DiscordPostNode,
    "wolfram.simple": WolframSimpleNode,
    "youtube.search": YouTubeSearchNode,
    "youtube.play": YouTubePlayNode,
    "sfx.play": SoundEffectNode,
    "output.tts": OutputTTSNode,
    "volume.set": VolumeSetNode,
    "giphy.search": GiphySearchNode,
    "done": DoneNode,
}
