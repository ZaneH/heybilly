import logging
import os

from openai import OpenAI

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PERSONALITY_MODEL_ID = os.getenv('PERSONALITY_MODEL_ID')

SYSTEM_PROMPT = """Your job is to be a home assistant. You are trained
on how to respond to requests from users. You will always respond with a
JSON dict.

Your task is to only modify nodes with `node_uuid` and only edit/attach the
'text' field. The text field should be a string. Make the length of your
response appropriate for the output node. Try to keep your answers short and
concise. Your output for each node will be given directly to the user, you
must fill in any placeholders with the correct data by using data from
previous nodes. Especially make sure that `output.tts` nodes have all the
info a user would expect to hear back.

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
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)

    def suggest_edits(self, prompt: str) -> str:
        logging.info("🗣️ Adding personality")
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
            ], model=PERSONALITY_MODEL_ID
        )

        return res.choices[0].message.content
