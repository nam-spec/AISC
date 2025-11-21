from collections import deque

class MazeAgent:

    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

    def is_valid(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols and self.maze[r][c] != 1

    def bfs_search(self, start, goal):
        queue = deque([(start, [start])])
        visited = set()

        while queue:
            (r, c), path = queue.popleft()

            if (r, c) == goal:
                return path

            if (r, c) in visited:
                continue
            visited.add((r, c))

            # Actions / moves
            moves = [(0,1), (1,0), (0,-1), (-1,0)]  # Right, Down, Left, Up

            for dr, dc in moves:
                nr, nc = r + dr, c + dc
                if self.is_valid(nr, nc):
                    queue.append(((nr, nc), path + [(nr, nc)]))

        return None


# ---------------- Simulation ----------------
maze = [
    [0, 0, 1, 0],
    [1, 0, 1, 0],
    [0, 0, 0, 0],
    [0, 1, 1, 0]
]

agent = MazeAgent(maze)

start = (0, 0)
goal = (3, 3)

path = agent.bfs_search(start, goal)

print("Shortest Path:", path)
