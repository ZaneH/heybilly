import json
import os

from openai import OpenAI

from src.graph.action_node import ActionNode
from src.graph.nodes.discord_post import DiscordPostNode
from src.graph.nodes.done import DoneNode
from src.graph.nodes.giphy_search import GiphySearchNode
from src.graph.nodes.input_voice import InputVoiceNode
from src.graph.nodes.twitter_post import TwitterPostNode
from src.graph.nodes.user_text_prompt import UserTextPromptNode
from src.graph.nodes.volume_up import VolumeUpNode

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
SYSTEM_PROMPT = """Create a JSON node graph for workflow actions:

- Begin with 'input.voice' for initial voice commands.
- Proceed with nodes relevant to the command's intent.
- Use 'user_text_prompt' for essential text inputs.
- Employ action nodes (e.g., 'twitter.post', 'discord.post', 'volume.up', 'youtube.search') for specific tasks.
- Allow nodes to output to multiple successors.
- Conclude each workflow with 'done'.

Example output:
```
{
  "nodes": {
    "1": {
      "type": "input.voice",
      "data": "Initial voice command.",
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
- user_text_prompt {prompt: String}: [Input: String; Outputs: String] Requests and outputs user text.
- twitter.post {text: String}: [Input: String; Outputs: Boolean] Posts to Twitter, outputs confirmation.
- discord.post {text: String}: [Input: String; Outputs: Boolean] Posts to Discord, outputs confirmation.
- wolfram.simple {query: String}: [Input: String; Outputs: String] Queries data, outputs result. Use for dynamic things like weather, finance, math, time, sports, etc.
- youtube.search {query: String, shuffle: Boolean}: [Input: String, Boolean; Outputs: Array] Searches YouTube, outputs video list.
- output.tts {text: String}: [Input: String; Outputs: Boolean] Converts text to speech. Outputs confirmation.
- volume.up: [No input; Outputs: Boolean] Increases volume, outputs confirmation.
- done: [No input, No output] Marks workflow completion.

Workflow Examples:
1. Tweet Creation: 'input.voice' -> 'user_text_prompt' -> 'twitter.post' -> 'done'.
2. Volume & Discord Meme Post: 'input.voice' -> 'volume.up' & 'giphy.search' -> 'discord.post' -> 'done'.
3. YouTube Video Query: 'input.voice' -> 'youtube.search' -> 'discord.post' -> 'done'.

Ensure workflows logically flow from 'input.voice' to 'done'.

Create a graph for the following request:

Hey Billy, post a random fact about cars to Discord."""

node_type_mapping = {
    "input.voice": InputVoiceNode,
    "user_text_prompt": UserTextPromptNode,
    "twitter.post": TwitterPostNode,
    "discord.post": DiscordPostNode,
    "giphy.search": GiphySearchNode,
    "volume.up": VolumeUpNode,
    "done": DoneNode
}

ai_sample_content = '''{
  "nodes": {
    "1": {
      "type": "input.voice",
      "data": "Hey Billy, turn the volume up and post a car meme to Discord.",
      "outputs": ["2"]
    },
    "2": {
      "type": "volume.up",
      "outputs": ["3"]
    },
    "3": {
      "type": "giphy.search",
      "query": "car",
      "shuffle": true,
      "outputs": ["4"]
    },
    "4": {
      "type": "discord.post",
      "outputs": ["5"]
    },
    "5": {
      "type": "done"
    }
  }
}'''


class GraphBuilder:
    def __init__(self):
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)

    def build_graph(self, prompt: str) -> ActionNode:
        print("User prompt:", prompt)
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
                model="ft:gpt-3.5-turbo-1106:startup::8lQF99eO"
            )

            ai_content = res.choices[0].message.content
        else:
            ai_content = ai_sample_content

        try:
            return GraphBuilder._create_nodes_from_json(ai_content)
        except:
            print("Invalid graph response. Please try again.")
            print("Graph:", ai_content)

            return None

    @staticmethod
    def _create_nodes_from_json(json_str):
        try:
            data = json.loads(json_str)
            nodes = {}

            # Create nodes using the specific subclass based on the type
            for node_id, node_info in data["nodes"].items():
                node_type = node_info["type"]
                node_class = node_type_mapping.get(node_type, ActionNode)
                nodes[node_id] = node_class(
                    node_id, node_type, [], node_info.get("outputs", []))

                # Add data to the node with any remaining keys
                extra_data = {}
                for key, value in node_info.items():
                    if key not in ["type", "outputs"]:
                        extra_data[key] = value

                setattr(nodes[node_id], "data", extra_data)

            # Link nodes
            for node in nodes.values():
                node.outputs = [nodes[out_id]
                                for out_id in node.outputs if out_id in nodes]

            return nodes
        except:
            print("Error in _create_nodes_from_json.")
            print(json_str)
            return None
