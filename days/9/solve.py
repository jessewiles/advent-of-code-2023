import functools
import sys
from typing import Callable


def load(filename: str):
    with open(filename, "r") as f:
        return f.read().splitlines(keepends=False)


def calc(data: list[str], end_index: int, reduce_func: Callable):
    tots: list[int] = list()
    for line in data:
        # setup
        stack = [[int(n) for n in line.split()]]
        inproc = stack[-1]
        newl: list[int] = list()
        stack.append(newl)

        # build the stack
        while True:
            for i in range(len(inproc) - 1):
                newl.append(inproc[i + 1] - inproc[i])
            if all([n == 0 for n in newl]):
                break
            else:
                inproc = newl
                newl = list()
                stack.append(newl)

        # calculate the total
        # TODO: Try storing the totals while building the stack
        vals = [x[end_index] if len(x) > 0 else 0 for x in stack]
        vals.reverse()
        tots.append(functools.reduce(reduce_func, vals, 0))
    return tots


def part1(data: list[str]):
    return sum(calc(data, -1, lambda x, y: x + y))


def part2(data: list[str]):
    return sum(calc(data, 0, lambda x, y: y - x))


if __name__ == "__main__":
    data = load(sys.argv[1])
    print(part1(data))
    print(part2(data))
