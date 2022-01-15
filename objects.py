from random import randint
import copy


class Cell:
    state = None

    def __init__(self, val=None) -> None:
        if val == None:
            val = randint(0, 2)
        self.state = val

    def __str__(self) -> str:
        if self.state == 0:
            return ' '
        if self.state == 1:
            return '.'
        if self.state == 2:
            return '*'


class World:
    height = None
    width = None
    content = None

    def __init__(self, height, width, content=None) -> None:
        if content != None:
            self.content = content
        else:
            self.content = [[0] * width for _ in range(height)]
            for i in range(height):
                for j in range(width):
                    self.content[i][j] = Cell()
        self.height = height
        self.width = width

    def __str__(self) -> str:
        return '\n'.join([' '.join(map(str, row))
                          for row in self.content])

    def count_alive_cells(self) -> int:
        count = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.content[i][j].state:
                    count += 1
        return count

    def count_alive_neighbors(self, y, x) -> int:
        def cell_neighbors(y: int, x: int) -> None:
            neighbors = []
            for i in range(y - 1, y + 2):
                for j in range(x - 1, x + 2):
                    if not (y == i and x == j):
                        neighbors.append([i, j])
            return neighbors
        count = 0
        neighbors = cell_neighbors(y, x)
        for neighbor in neighbors:
            y, x = neighbor
            if x < 0 or y < 0 or \
                    x >= self.width or \
                    y >= self.height:
                continue
            if self.content[y][x].state == 2:
                count += 1
        return count

    def copy(self):
        return copy.deepcopy(self)

    def next_epoch(self) -> None:
        prev_world = self.copy()
        for i in range(self.height):
            for j in range(self.width):
                cell = prev_world.content[i][j]
                neighbors_alive = prev_world.count_alive_neighbors(i, j)
                if cell.state == 2:
                    if not 1 < neighbors_alive < 4:
                        self.content[i][j].state = 1
                else:
                    self.content[i][j].state = 0
                    if neighbors_alive == 3:
                        self.content[i][j].state = 2
