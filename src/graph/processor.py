class GraphProcessor:
    def __init__(self, graph):
        self.graph = graph
        self.current_node = "1"

        print("GraphProcessor initialized with:", graph)

    async def start(self):
        await self.graph[self.current_node].process()
