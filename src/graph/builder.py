import json
import logging
import os

from src.graph.action_node import ActionNode
from src.graph.node_map import NODE_MAP
from src.graph.validator import GraphValidator, NodeIOValidationError
from src.utils.openai_helper import OpenAIHelper

BUILDER_MODEL_ID = os.getenv("BUILDER_MODEL_ID")
SYSTEM_PROMPT = """Create a JSON node graph for workflow actions:

- Begin with 'input.voice' for initial voice commands.
- Proceed with nodes relevant to the command's intent.
- Use 'user_text_prompt' for essential text inputs.
- Employ only the provided node types.
- End each graph for the workflow with 'done'.

- Searches should be excluded unless they are used later.
- Do *NOT* use any placeholder text.
- Try to create simple graphs instead of long and complex ones.
- Ensure there is a path from 'input.voice' to 'done' only once in the graph.
- Branches that end in 'dead-end nodes' should not obstruct or interfere with the main flow reaching 'done'.

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
- discord.post {text: String}: [Input: String] Posts to Discord. Supports some markdown.
- wolfram.simple {query: String}: [Input: String; Outputs: String] Queries real-time data, outputs result. It's expensive but accurate.
- giphy.search {query: String, shuffle: Boolean}: [Input: String, Boolean; Outputs: String] Queries Giphy, outputs GIF URL. Use full words to get back results.
- pexels.search {query: String, count: Integer, shuffle: Boolean}: [Input: String, Boolean; Outputs: Array] Search stock photos on Pexels, outputs image URL.
- youtube.search {query: String, shuffle: Boolean}: [Input: String, Boolean; Outputs: String] Searches YouTube, outputs video list.
- sfx.play {video_id: String}: [Input: String] Plays short sound effect for 5s.
- output.tts {text: String}: [Input: String; Outputs: String] Play text to speech using 'text'.
- volume.set {value: String}: [Input: String] Set/increase/decrease the volume. Only: values 0 thru 10, '+', or '-'.
- music.control {action: String}: [Input: String, Boolean] Start/resume/pause/stop music. Only: 'start', 'play', 'pause', or 'stop'. Start requires a YouTube search node before it.
- hn.top: [No input; Outputs: Array] Outputs Top 10 Hacker News posts.
- nyt.top: [No input; Outputs: Array] Outputs Top 10 New York Times posts.
- tradingview.chart {symbol: String, interval: String, crypto: Boolean}: [Input: String, String, Boolean; Outputs: String] Outputs pre-filled TradingView URL for stocks and crypto.
- done: [Input: Any] Marks workflow completion. 1 per graph.

Workflow Examples:
1. Tweet Creation: 'input.voice' -> 'user_text_prompt' -> 'twitter.post' -> 'done'.
2. Volume & Discord Meme Post: 'input.voice' -> 'volume.set' & 'giphy.search' -> 'discord.post' -> 'done'.
3. YouTube Video Query: 'input.voice' -> 'youtube.search' -> 'discord.post' -> 'done'.

Ensure workflows there is a path from 'input.voice' to 'done' only once in the graph."""

ai_sample_content = None
unused_1 = '''{
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
unused_2 = """
- user_text_prompt {prompt: String}: [Input: String; Outputs: String] Requests and outputs user text. Exclusively for making posts.
- twitter.post {text: String}: [Input: String] Posts to Twitter."""


class GraphBuilder:
    def __init__(self):
        self.openai_helper = OpenAIHelper()

    def build_graph(self, prompt: str):
        logging.info(f"User prompt: {prompt}")
        if not ai_sample_content:
            graph_builder_response = self.openai_helper.get_completion(
                SYSTEM_PROMPT, prompt, model=BUILDER_MODEL_ID
            )

            ai_content = graph_builder_response
        else:
            ai_content = ai_sample_content

        logging.debug(f'---\nGraph Builder:\n{ai_content}\n---')

        return ai_content

    @staticmethod
    def _create_nodes_from_json(json_str, graph_processor):
        try:
            try:
                data = json.loads(json_str, strict=False)
            except json.JSONDecodeError:
                # Hack to fix a simple mistake by the AI. There may be more to come.
                json_str += "}"
                data = json.loads(json_str, strict=False)

            # Initial node validation (types)
            GraphValidator.validate_nodes(data)
            nodes = {}

            # Create nodes using the specific subclass based on the type
            for node_id, node_info in data["nodes"].items():
                node_type = node_info["type"].lower().strip()
                node_class = NODE_MAP.get(node_type, ActionNode)
                nodes[node_id] = node_class(node_id, node_type, node_info.get(
                    "inputs", []), node_info.get("outputs", []))

                # Add node.data[...] to the node with any remaining keys
                extra_data = {}
                for key, value in node_info.items():
                    if key not in ["type", "outputs"]:
                        extra_data[key] = value

                setattr(nodes[node_id], "data", extra_data)

                # Having a reference to the graph processor is useful
                setattr(nodes[node_id], "graph_processor", graph_processor)

            # Link nodes
            for node in nodes.values():
                node.outputs = [nodes[out_id]
                                for out_id in node.outputs if out_id in nodes]

            GraphValidator.validate_node_io(nodes)

            return nodes
        except NodeIOValidationError as e:
            logging.debug("Error validating node connections.")
            logging.debug(e)
            raise e
        except Exception as e:
            logging.debug("Error turning JSON into nodes.")
            logging.debug(e)
            raise e
