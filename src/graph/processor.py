class GraphProcessor:
    def __init__(self, graph):
        self.graph = graph
        self.current_node = "1"

    def pretty_print(self):
        print("Graph:")
        for node in self.graph.values():
            print("    ", node)

    async def start(self):
        try:
            await self.graph[self.current_node].process()
        except Exception as e:
            print("Error processing graph:", e)
            print(self.pretty_print())
