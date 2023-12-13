import math
import sys


def load_input(filename: str):
    sequence = str()
    nodes: dict[str, dict[str, str]] = dict()
    starters: list[str] = list()
    with open(filename) as f:
        sequence = f.readline().strip()
        f.readline()
        for line in f:
            line = line.strip()
            if not line:
                break
            key, _, suffix = line.partition(" = ")
            left, right = suffix.replace("(", "").replace(")", "").split(", ")
            nodes[key] = {"L": left, "R": right}
            if key.endswith("A"):
                starters.append(key)

        return sequence, starters, nodes


def part1(data: tuple[str, list[str], dict[str, dict[str, str]]]):
    sequence, _, nodes = data

    hops = 1
    idx = 0
    point = nodes["AAA"][sequence[idx]]
    while point != "ZZZ":
        idx += 1
        if idx == len(sequence):
            idx = 0
        hops += 1
        point = nodes[point][sequence[idx]]

    return hops


def part2(data: tuple[str, list[str], dict[str, dict[str, str]]]):
    sequence, starters, nodes = data
    starter_hops: list[int] = list()

    for node in starters:
        hops = 1
        idx = 0
        point = nodes[node][sequence[idx]]
        while not point.endswith("Z"):
            idx += 1
            if idx == len(sequence):
                idx = 0
            hops += 1
            point = nodes[point][sequence[idx]]
        starter_hops.append(hops)

    return math.lcm(*starter_hops)


if __name__ == "__main__":
    data = load_input(sys.argv[1])
    print(part1(data))
    data = load_input(sys.argv[2])
    print(part2(data))
