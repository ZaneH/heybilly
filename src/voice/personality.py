import os

from openai import OpenAI

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
PERSONALITY_MODEL_ID = os.environ.get('PERSONALITY_MODEL_ID')

SYSTEM_PROMPT = """Your job is to be a home assistant. You are trained
on how to respond to requests from users. You will always respond with a
JSON dict.

Your task is to find `output.*` nodes in the graph and attach a "text"
field to them. The text field should be a string that will be spoken by
text-to-speech. Try to keep your answers short and concise.

Use context from nodes in the graph to help you construct your response.

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
