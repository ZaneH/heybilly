import os
import random

import giphy_client

from src.graph.action_node import ActionNode, DataTypes

GIPHY_API_KEY = os.getenv('GIPHY_API_KEY')


class GiphySearchNode(ActionNode):
    create_queue = False

    input_data_type = {DataTypes.STRING}
    output_data_type = {DataTypes.URL}

    async def execute(self, input_data=None):
        query = self.data['query']
        if not query:
            raise Exception("No Giphy search query provided")

        shuffle = self.data.get('shuffle', False)
        limit = 1
        if shuffle:
            limit = 10

        client = giphy_client.DefaultApi()
        res = client.gifs_search_get(GIPHY_API_KEY, query, limit=limit)

        if shuffle:
            return random.choice(res.data).images.original.url

        return res.data[0].images.original.url

    def validate_inputs(self) -> bool:
        """
        Validate that query was provided in the data field
        """
        if 'query' not in self.data:
            return False

        return True
