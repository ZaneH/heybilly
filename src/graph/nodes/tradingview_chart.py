from src.graph.action_node import ActionNode, NodeIODataType


class TradingViewChartNode(ActionNode):
    create_queue = False

    input_data_type = {NodeIODataType.NONE}

    async def execute(self, input_data=None):
        symbol = self.data['symbol']
        interval = str(self.data.get('interval', '1D')).upper()
        # TODO: Validate the interval (or use a fallback)

        chart_url = f"https://www.tradingview.com/chart/?symbol={symbol}&interval={interval}"
        self.data['result'] = chart_url

        self.graph_processor.has_stale_text = True

        return chart_url

    def validate_inputs(self) -> bool:
        """
        Validate that text was provided in the data field
        """
        if 'text' not in self.data:
            return False

        return True
