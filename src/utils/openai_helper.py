import os
from openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class OpenAIHelper:
    def __init__(self):
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)

    def get_completion(self, system, user, model='gpt-3.5-turbo-1106', **kwargs):
        res = self.openai_client.chat.completions.create(messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": user
            }
        ], model=model, **kwargs)

        return res.choices[0].message.content
