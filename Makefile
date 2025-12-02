# GENERATORS = {
#     "spanning-tree": SpanningTreeGenerator,
#     "binary-tree": BinaryTreeGenerator,
#     "random-growth": RandomGrowthGenerator,
# }

# SOLVERS = {
#     "bfs": BreadthFirstSolver,
#     "dfs": DepthFirstSolver,
#     "dijkstra": DijkstraSolver,
# }

# Конфигурация лабиринта
WIDTH := 100
HEIGHT := 100
START_X := 5
START_Y := 5
GENERATOR := random-growth
# GENERATOR := binary-tree
# GENERATOR := spanning-tree
EXPORT_FILE := web/data/latest.json

# Алгоритм Дейкстры (Dijkstra)
dij:
	uv run main.py \
		--start $(START_X) $(START_Y) \
		--width $(WIDTH) --height $(HEIGHT) \
		--export-json $(EXPORT_FILE) \
		--generator $(GENERATOR) \
		--solver dijkstra

# Поиск в ширину (BFS)
bfs:
	uv run main.py \
		--start $(START_X) $(START_Y) \
		--width $(WIDTH) --height $(HEIGHT) \
		--export-json $(EXPORT_FILE) \
		--generator $(GENERATOR) \
		--solver bfs

# Поиск в глубину (DFS)
dfs:
	uv run main.py \
		--start $(START_X) $(START_Y) \
		--width $(WIDTH) --height $(HEIGHT) \
		--export-json $(EXPORT_FILE) \
		--generator $(GENERATOR) \
		--solver dfs



server:
	python3 -m http.server 8000
