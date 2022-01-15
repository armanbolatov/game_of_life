import time
import os
from objects import World, Cell
from messages import messages


def fill_content(content, height, width) -> bool:
    for _ in range(height):
        line, row = input(), []
        if len(line) != width:
            print(messages['line_length_error'])
            return False
        for char in line:
            if char == '0':
                row.append(Cell(0))
            elif char == '1':
                row.append(Cell(2))
            else:
                print(messages['line_char_error'])
                return False
        content.append(row)
    return True


def main():
    height, width = map(int, input(messages['world_size']).split())
    manual = input(messages['manual'])
    while not manual in ['y', 'n', 'Y', 'N']:
        manual = input(messages['manual_error'])
    if manual in ['y', 'Y']:
        print(messages['write_world'])
        content = []
        while not fill_content(content, height, width):
            content = []
        world = World(height, width, content=content)
    else:
        world = World(height, width)

    def clear(): return os.system('cls')
    clear()
    while True:
        print(world)
        time.sleep(0.125)
        clear()
        world.next_epoch()


if __name__ == "__main__":
    main()
