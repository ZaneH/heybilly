import random
import feedparser

from src.graph.action_node import ActionNode, NodeIODataType


class NYTTopNode(ActionNode):
    create_queue = False

    output_data_type = {NodeIODataType.OBJECT}

    async def execute(self, input_data=None):
        feed = feedparser.parse(
            'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml')

        random.shuffle(feed['entries'])
        top_10 = feed['entries'][:10]
        results = []

        for entry in top_10:
            results.append({
                'title': entry['title'],
                'link': entry['link']
            })

        self.data['results'] = results

        self.graph_processor.has_stale_text = True

        return results

    def validate_inputs(self) -> bool:
        return True
