import os
import random
from pexels_api import API as PexelsAPI
from src.graph.action_node import ActionNode, NodeIODataType

PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')


class PexelsSearchNode(ActionNode):
    create_queue = False

    input_data_type = {NodeIODataType.NONE}
    output_data_type = {NodeIODataType.URL}

    async def execute(self, input_data=None):
        client = PexelsAPI(PEXELS_API_KEY)

        shuffle = self.data.get('shuffle', False)
        query = self.data['query']
        count = self.data.get('count', 1)

        if not query:
            raise Exception("No Pexels search query provided")

        client.search(
            query=query,
            results_per_page=count
        )

        results = client.get_entries()
        if not results:
            raise Exception("No results found for Pexels search query")

        if shuffle:
            random.shuffle(results)

        self.graph_processor.has_stale_text = True

        original_urls = []
        for result in results:
            original_urls.append(result.compressed)

        self.data['results'] = original_urls

        return result

    def validate_inputs(self) -> bool:
        """
        Validate that value was provided in the data field
        """
        if 'value' not in self.data:
            return False

        return True
