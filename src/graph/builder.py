import json
import logging
import os

from openai import OpenAI

from src.graph.action_node import ActionNode
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

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
BUILDER_MODEL_ID = os.environ.get("BUILDER_MODEL_ID")
SYSTEM_PROMPT = """Create a JSON node graph for workflow actions:

- Begin with 'input.voice' for initial voice commands.
- Proceed with nodes relevant to the command's intent.
- Use 'user_text_prompt' for essential text inputs.
- Employ only the provided node types.
- End each graph for the workflow with 'done'.

- Searches should be excluded unless they are used later.
- Do *NOT* use any placeholder text. (like {{input}} or %1%)
- Try to create simple graphs instead of long and complex ones.
- Ensure there is a path from 'input.voice' to 'done' only once in the graph. Branches that end in "dead-end nodes" should not obstruct or interfere with the main flow reaching 'done'.

Example output:
```
{
  "nodes": {
    "1": {
      "type": "input.voice",
      "text": "Initial voice command.",
      "outputs": ["2"]
    },
    // More nodes here
    "N": {
      "type": "done"
    }
  }
}
```

Node Types:
- input.voice: [No input; Outputs: String] User input node. Spoken.
- user_text_prompt {prompt: String}: [Input: String; Outputs: String] Requests and outputs user text. Exclusively for making posts.
- twitter.post {text: String}: [Input: String] Posts to Twitter.
- discord.post {text: String}: [Input: String] Posts to Discord.
- wolfram.simple {query: String}: [Input: String; Outputs: String] Queries real-time data, outputs result. It's expensive but accurate.
- giphy.search {query: String, shuffle: Boolean}: [Input: String, Boolean; Outputs: Array] Queries Giphy, outputs GIF URL. Use full words to get back results.
- youtube.search {query: String, shuffle: Boolean}: [Input: String, Boolean; Outputs: Array] Searches YouTube, outputs video list.
- youtube.play {video_id: String}: [Input: String] Plays YouTube video.
- sfx.play {video_id: String}: [Input: String] Plays sound effect for 5s.
- output.tts {text: String}: [Input: String] Play text to speech using "text".
- volume.set {value: String}: [Input: String] Set/increase/decrease the volume. Only: values 0 thru 10, "+", or "-".
- done: [Input: Any] Marks workflow completion.

Workflow Examples:
1. Tweet Creation: 'input.voice' -> 'user_text_prompt' -> 'twitter.post' -> 'done'.
2. Volume & Discord Meme Post: 'input.voice' -> 'volume.set' & 'giphy.search' -> 'discord.post' -> 'done'.
3. YouTube Video Query: 'input.voice' -> 'youtube.search' -> 'discord.post' -> 'done'.

Ensure workflows there is a path from 'input.voice' to 'done' only once in the graph."""

ai_sample_content = None
'''{
  "nodes": {
    "1": {
      "type": "input.voice",
      "text": "Yo Billy, find out what the price of gold is and post it to the Discord.",
      "outputs": ["2"]
    },
    "2": {
      "type": "wolfram.simple",
      "query": "Price of gold",
      "outputs": ["3"]
    },
    "3": {
      "type": "discord.post",
      "text": "Here's the current price for gold: {{input}}",
      "outputs": ["4"]
    },
    "4": {
      "type": "done"
    }
  }
}'''


class GraphBuilder:
    def __init__(self):
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)

    def build_graph(self, prompt: str, verbose=False) -> ActionNode:
        logging.info(f"User prompt: {prompt}")
        if not ai_sample_content:
            res = self.openai_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                model=BUILDER_MODEL_ID
            )

            ai_content = res.choices[0].message.content
        else:
            ai_content = ai_sample_content

        if verbose:
            logging.debug(f'---\nGraph Builder:\n{ai_content}\n---')

        return ai_content

    @staticmethod
    def _create_nodes_from_json(json_str, graph_processor):
        try:
            data = json.loads(json_str)
            nodes = {}

            # Create nodes using the specific subclass based on the type
            for node_id, node_info in data["nodes"].items():
                node_type = node_info["type"]
                node_class = NODE_MAP.get(node_type, ActionNode)
                nodes[node_id] = node_class(node_id, node_type, node_info.get(
                    "inputs", []), node_info.get("outputs", []))

                # Add data to the node with any remaining keys
                extra_data = {}
                for key, value in node_info.items():
                    if key not in ["type", "outputs"]:
                        extra_data[key] = value

                setattr(nodes[node_id], "data", extra_data)
                setattr(nodes[node_id], "graph_processor", graph_processor)

            # Link nodes
            for node in nodes.values():
                node.outputs = [nodes[out_id]
                                for out_id in node.outputs if out_id in nodes]

            return nodes
        except:
            logging.error("Error turning JSON into nodes.")
            logging.error(json_str)
            return None
