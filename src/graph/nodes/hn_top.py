import feedparser

from src.graph.action_node import ActionNode, DataTypes


class HNTopNode(ActionNode):
    create_queue = False

    input_data_type = {DataTypes.NONE}
    output_data_type = {DataTypes.OBJECT}

    async def execute(self, input_data=None):
        feed = feedparser.parse('https://hnrss.org/frontpage')
        top_10 = feed['entries'][:10]
        results = []

        for entry in top_10:
            results.append({
                'title': entry['title'],
                'link': entry['link'],
            })

        self.data['results'] = results

        self.graph_processor.has_stale_text = True

        return results

    def validate_inputs(self) -> bool:
        return True
