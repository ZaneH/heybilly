import os
import wolframalpha
from src.graph.action_node import ActionNode

WOLFRAM_APP_ID = os.environ.get('WOLFRAM_APP_ID')


class WolframSimpleNode(ActionNode):
    create_queue = False

    async def execute(self, input_data=None):
        query = self.data['query']
        if not query:
            raise Exception("No WolframAlpha query provided")

        client = wolframalpha.Client(WOLFRAM_APP_ID)
        res = client.query(query)

        self.graph_processor.has_stale_text = True
        return next(res.results).text

    def validate_inputs(self) -> bool:
        """
        Validate that query was provided in the data field
        """
        if 'query' not in self.data:
            return False

        return True
