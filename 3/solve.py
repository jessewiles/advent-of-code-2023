from collections import defaultdict
from math import prod


def part1():
    grid = []
    with open("input.txt") as f:
        for line in f.readlines():
            grid.append(list(line.strip()))
    width = len(grid[0])
    height = len(grid)
    parts = []
    gears = defaultdict(list)
    for i in range(height):
        # in_range = False
        active_number = []
        active_range = []
        for j in range(width):
            char = grid[i][j]
            if char.isnumeric():
                # in_range = True
                active_number.append(char)
                active_range.append((i, j))
                if j + 1 == width:
                    has_adjacent_symbol, coord, char = adjacent_symbol_info(
                        active_range, grid
                    )
                    if has_adjacent_symbol:
                        num = int("".join(active_number))
                        parts.append(num)
                        if char == "*":
                            gears[coord].append(num)
            else:
                has_adjacent_symbol, coord, char = adjacent_symbol_info(
                    active_range, grid
                )
                if has_adjacent_symbol:
                    # print(active_range)
                    # print(active_number)
                    num = int("".join(active_number))
                    parts.append(int("".join(active_number)))
                    if char == "*":
                        gears[coord].append(num)
                # in_range = False
                active_range = []
                active_number = []
    # print(parts)
    print(sum(parts))
    actual_gears = [prod(gear) for gear in gears.values() if len(gear) == 2]
    print(sum(actual_gears))


def adjacent_symbol_info(
    active_range: list[tuple[int, int]], grid: list[list[str]]
) -> tuple[bool, tuple[int, int], str]:
    for coord in active_range:
        x, y = coord
        adjacencies = [
            (x - 1, y),  # west
            (x + 1, y),  # east
            (x, y - 1),  # north
            (x, y + 1),  # south
            (x - 1, y + 1),  # southwest
            (x + 1, y + 1),  # southeast
            (x - 1, y - 1),  # northwest
            (x + 1, y - 1),  # northeast
        ]
        for ax, ay in adjacencies:
            if ax < 0 or ay < 0:
                continue
            try:
                if char_is_symbol(grid[ax][ay]):
                    return (True, (ax, ay), grid[ax][ay])
            except IndexError:
                continue
    return (False, (-1, -1), "")


def char_is_symbol(char: str) -> bool:
    return not char.isnumeric() and char != "."


if __name__ == "__main__":
    part1()
