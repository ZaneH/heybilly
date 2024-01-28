import os
import random

from pyyoutube import Client

from src.graph.action_node import ActionNode

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


class YouTubeSearchNode(ActionNode):
    create_queue = False

    async def execute(self, input_data=None):
        client = Client(api_key=GOOGLE_API_KEY)
        shuffle = self.data.get('shuffle', False)
        query = self.data['query']

        if not query:
            raise Exception("No YouTube search query provided")

        limit = 1
        if shuffle:
            limit = 10

        search_response = client.search.list(
            q=query,
            part='snippet',
            maxResults=limit
        )

        url_prefix = 'https://www.youtube.com/watch?v='
        video_id = search_response.items[0].id.videoId

        if shuffle:
            video_id = random.choice(search_response.items).id.videoId

        return url_prefix + video_id

    def validate_inputs(self) -> bool:
        """
        Validate that query was provided in the data field
        """
        if 'query' not in self.data:
            return False

        return True
