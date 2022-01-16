from random import randint
import copy


class Cell:
    """
    Класс клетки игрового поля. Имеет параметр state, который
    определяет его состояние. Если state = 2, то клетка жива;
    если state = 1, то клетка при смерти (должна умереть на
    следующем ходу); если state = 0, то клетка мертва.
    """
    state = None

    def __init__(self, val=None) -> None:
        # если не задано значение, то инициализируем рандомно
        if val == None:
            val = randint(0, 2)
        self.state = val

    def __str__(self) -> str:
        # отображаем состояние клетки
        if self.state == 0:
            return ' '
        if self.state == 1:
            return '.'
        if self.state == 2:
            return '*'


class World:
    """
    Класс игрового мира состоящего из клеток. Имеет параметры:
    height, width - целые числа выражающие размеры игрового мира,
    content - матрица размера height * width состоящая из Cell.
    """
    height = None
    width = None
    content = None

    def __init__(self, height, width, content=None) -> None:
        if content != None:
            self.content = content
        else:
            # если не задан мир, то инициализировать рандомно
            self.content = [[0] * width for _ in range(height)]
            for i in range(height):
                for j in range(width):
                    self.content[i][j] = Cell()
        self.height = height
        self.width = width

    def __str__(self) -> str:
        # отображение игрового мира отделяя клетки пробелом
        return '\n'.join([' '.join(map(str, row))
                          for row in self.content])

    def count_alive_neighbors(self, y, x) -> int:
        # считает количество живых клеток возле клетки (x, y)
        def cell_neighbors(y: int, x: int) -> None:
            # выводит массив координат клеток соседей (x, y)
            neighbors = []
            for i in range(y - 1, y + 2):
                for j in range(x - 1, x + 2):
                    if not (y == i and x == j):
                        neighbors.append([i, j])
            return neighbors
        count = 0
        neighbors = cell_neighbors(y, x)
        # проверяем для каждой координаты соседа не выходит ли
        # клетка за рамки игрового мира, если нет и клетка жива,
        # то увеличиваем счетчик на единицу
        for neighbor in neighbors:
            y, x = neighbor
            if  x < 0 or y < 0 or \
                x >= self.width or \
                y >= self.height:
                continue
            if self.content[y][x].state == 2:
                count += 1
        return count

    def copy(self):
        # создает точную копию игрового мира
        return copy.deepcopy(self)

    def next_epoch(self) -> None: 
        # метод переводящий мир в следующую эпоху (итерацию)
        prev_world = self.copy()
        for i in range(self.height):
            for j in range(self.width):
                cell = prev_world.content[i][j]
                neighbors_alive = prev_world.count_alive_neighbors(i, j)
                if cell.state == 2:
                    # если клетка жива и количество соседей не в интервале
                    # [2, 3], то клетка должна умереть; ставим state = 1
                    if not 1 < neighbors_alive < 4:
                        self.content[i][j].state = 1
                else:
                    # если клетка мертва или при смерти, то в следующем ходу
                    # клетка умирает; ставим state = 0
                    self.content[i][j].state = 0
                    # однако, если количество соседей оказалось равно 3,
                    # то клетка становится живой; ставим state = 2
                    if neighbors_alive == 3:
                        self.content[i][j].state = 2
