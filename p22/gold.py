import heapq
from itertools import product


def show(risk, tx, ty):

    for j in range(ty+2):
        row = []
        for i in range(tx+2):
            s = {0: '.', 1: '=', 2: '|'}
            if (i, j) == (0, 0):
                row.append('M')
            elif (i, j) == (tx, ty):
                row.append('T')
            else:
                row.append(s[risk[(i, j)]])
        print(''.join(row))


def build_cave(depth, tx, ty):

    geologic = {}
    erosion = {}

    EXTRA_SIZE = 100

    for i in range(tx + EXTRA_SIZE):
        geologic[(i, 0)] = i * 16807
        erosion[(i, 0)] = (geologic[(i, 0)] + depth) % 20183

    for j in range(ty + EXTRA_SIZE):
        geologic[(0, j)] = j * 48271
        erosion[(0, j)] = (geologic[(0, j)] + depth) % 20183

    for i, j in product(range(1, tx+EXTRA_SIZE), range(1, ty+EXTRA_SIZE)):
        geologic[(i, j)] = erosion[(i-1, j)] * erosion[(i, j-1)]
        erosion[(i, j)] = (geologic[(i, j)] + depth) % 20183

    geologic[(0, 0)] = 0
    geologic[(tx, ty)] = 0
    erosion[(0, 0)] = 0
    erosion[(tx, ty)] = 0

    risk = {k: v % 3 for k, v in erosion.items()}

    return risk


class AStar:

    def __init__(self, cave, target):

        self.target = target
        self.graph = cave

        self.max_x = max(x[0] for x in cave)
        self.max_y = max(x[1] for x in cave)

        self.best_cost = {((0, 0), 'torch'): 0}
        self.neighbors = [(0, ((0, 0), 'torch'))]
        self.visited = set()

    def search(self):

        while self.neighbors:

            t, next_node = heapq.heappop(self.neighbors)
            if t >= self.best_cost.get(self.target, 9E99):
                break
            if next_node in self.visited:
                continue
            self._visit_node(next_node)

        return self.best_cost[self.target]

    def _visit_node(self, node):

        self.visited.add(node)

        (nx, ny), tool = node

        # neighbors by walking
        for _x, _y in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            x = nx + _x
            y = ny + _y

            if any([(x < 0), (y < 0), (x >= self.max_x), (y >= self.max_y)]):
                continue

            # right tool for da job?
            risk = self.graph[(x, y)]

            if tool == 'none' and risk == 0:
                continue
            if tool == 'torch' and risk == 1:
                continue
            if tool == 'climbing' and risk == 2:
                continue

            g = self.best_cost[node] + 1
            h = self._heuristic(x, y)
            t = g + h

            self.best_cost[((x, y), tool)] = min(g, self.best_cost.get(((x, y), tool), 9E99))

            state = ((x, y), tool)
            if state not in self.visited:
                new_node = (t, state)
                heapq.heappush(self.neighbors, new_node)

        # neighbors by switching tool
        risk = self.graph[(nx, ny)]
        for new_tool in ['none', 'torch', 'climbing']:

            if new_tool == tool:
                continue
            if new_tool == 'none' and risk == 0:
                continue
            if new_tool == 'torch' and risk == 1:
                continue
            if new_tool == 'climbing' and risk == 2:
                continue

            g = self.best_cost[node] + 7
            h = self._heuristic(x, y)
            t = g + h

            self.best_cost[((nx, ny), new_tool)] = min(g, self.best_cost.get(((nx, ny), new_tool), 9E99))

            state = ((nx, ny), new_tool)
            if state not in self.visited:
                new_node = (t, state)
                heapq.heappush(self.neighbors, new_node)

    def _heuristic(self, x, y):
        return self.max_x - x + self.max_y - y


def solve(depth, tx, ty):

    cave = build_cave(depth, tx, ty)

    target = ((tx, ty), 'torch')
    a = AStar(cave, target)
    solution = a.search()

    show(cave, tx, ty)
    return solution


def main():

    with open("input") as in_f:
        d = int(in_f.readline().strip().split()[-1])
        tx, ty = map(int, in_f.readline().strip().split()[-1].split(','))

    solution = solve(d, tx, ty)

    print(solution)


if __name__ == "__main__":

    main()
