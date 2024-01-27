class GraphProcessor:
    def __init__(self, graph):
        self.graph = graph
        self.current_node = "1"

        # pretty print the graph
        print("Graph:")
        for node in self.graph.values():
            print("    ", node)

    async def start(self):
        await self.graph[self.current_node].process()
