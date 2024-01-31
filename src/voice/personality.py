import logging
import os

from src.utils.openai_helper import OpenAIHelper

PERSONALITY_MODEL_ID = os.getenv('PERSONALITY_MODEL_ID')

SYSTEM_PROMPT = """Your job is to be a home assistant. You are trained
on how to respond to requests from users. You will always respond with a
JSON dict.

Your task is to only modify nodes with `node_uuid` and only edit/attach the
'text' field. The text field should be a string. Make the length of your
response appropriate for the output node. Try to keep your answers short and
concise. Your output for each node will be given directly to the user, you
must fill in any placeholders and attach the correct data to 'text' by using
the result/results key from previous nodes. Especially make sure that
`output.tts` nodes have all the info a user would expect to hear back. Do
not add URLs to the `output.tts`.

Example output:
```
edits: [
    {
        "node_uuid": "abc421",
        "text": "Hello, world!"
    },
    {
        "node_uuid": "def610",
        "text": "Goodbye, world!"
    }
]
```"""


class Personality:
    def __init__(self) -> None:
        self.openai_helper = OpenAIHelper()

    def suggest_edits(self, prompt: str) -> str:
        logging.info("🗣️ Requesting personality")
        return self.openai_helper.get_completion(
            SYSTEM_PROMPT, prompt, model=PERSONALITY_MODEL_ID
        )
