import time
import os
from objects import World, Cell
from messages import messages


def fill_content(content, height, width) -> bool:
    """
    Заполняет массив content содержанием игрового мира 
    из строк введенных пользователем и возвращает True
    при успешном заполнении и False в случае ошибки.
    """
    for _ in range(height):
        line, row = input(), []
        if len(line) != width:
            # если введена строка размера больше чем ширина мира,
            # то выводим соответствующую ошибку
            print(messages['line_length_error'])
            return False
        for char in line:
            # посимвольно переводит строку список из Cell и
            # добавляет в массив content
            if char == '0':
                row.append(Cell(0))
            elif char == '1':
                row.append(Cell(2))
            else:
                # если в строке есть символ отличный от 0 и 1,
                # то выводим соответствующую ошибку
                print(messages['line_char_error'])
                return False
        content.append(row)
    return True


def main():
    # считаем размеры игрового мира
    height, width = map(int, input(messages['world_size']).split())
    # ручной ввод игрового мира или рандомная генерация
    manual = input(messages['manual'])
    while not manual in ['y', 'n', 'Y', 'N']:
        manual = input(messages['manual_error'])
    if manual in ['y', 'Y']:
        # заполняем игровое поле 
        print(messages['write_world'])
        content = []
        while not fill_content(content, height, width):
            content = []
        world = World(height, width, content=content)
    else:
        # рандомно создаем игровое поле
        world = World(height, width)

    # "чистит" консоль
    def clear(): return os.system('cls')
    clear()
    while True:
        # выводим мир, ждем 1/8 cекунды и обновляем мир
        print(world)
        time.sleep(0.125)
        clear()
        world.next_epoch()


if __name__ == "__main__":
    main()
