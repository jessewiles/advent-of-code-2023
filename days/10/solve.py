import copy
import sys


MOVES: dict[str, list[tuple]] = {
    "|": [((0, 1), ("|", "J", "L")), ((0, -1), ("|", "7", "F"))],
    "-": [((1, 0), ("-", "J", "7")), ((-1, 0), ("-", "F", "L"))],
    "L": [((1, 0), ("-", "J", "7")), ((0, -1), ("|", "7", "F"))],
    "J": [((-1, 0), ("-", "L", "F")), ((0, -1), ("|", "7", "F"))],
    "7": [((0, 1), ("|", "J", "L")), ((-1, 0), ("-", "F", "L"))],
    "F": [((0, 1), ("|", "J", "L")), ((1, 0), ("-", "7", "J"))],
}


def load(filename: str) -> tuple[list[list[str]], tuple[int, int]]:
    result: list[list[str]] = []
    start: tuple[int, int] = (-1, -1)
    with open(filename) as f:
        for idx, line in enumerate(f):
            raw = line.strip()
            row = list(raw)
            if "S" in raw:
                start = (raw.index("S"), idx)
            result.append(row)

    return result, start


def part1(data: tuple[list[list[str]], tuple[int, int]]) -> tuple[float, list[tuple]]:
    distances: list[list[tuple]] = []
    _map, start = data

    possible_loops = []
    for coord in (
        (start[0] + 1, start[1]),
        (start[0] - 1, start[1]),
        (start[0], start[1] + 1),
        (start[0], start[1] - 1),
    ):
        if coord[0] < 0 or coord[0] >= len(_map[0]):
            continue
        if coord[1] < 0 or coord[1] >= len(_map):
            continue
        sp = _map[coord[1]][coord[0]]
        if sp in MOVES and sp != "S":
            possible_loops.append(coord)

    for coord in possible_loops:
        visited = [start, coord]
        entry = coord
        kontinue = True
        while kontinue:
            for move in MOVES[_map[entry[1]][entry[0]]]:
                move_offset, allowable_move_chars = move
                move_coord = (entry[0] + move_offset[0], entry[1] + move_offset[1])
                if move_coord[0] < 0 or move_coord[0] >= len(_map[0]):
                    continue
                if move_coord[1] < 0 or move_coord[1] >= len(_map):
                    continue
                if move_coord == start and len(visited) > 2:
                    kontinue = False
                    distances.append(visited)
                    break

                move_char = _map[move_coord[1]][move_coord[0]]
                if move_coord not in visited and move_char in allowable_move_chars:
                    entry = move_coord
                    visited.append(move_coord)
                    break

    maxr = -1
    topv = []
    for v in distances:
        if len(v) > maxr:
            maxr = len(v)
            topv = v

    return (maxr / 2, topv)


def part2(dmap: list[list[str]], visited: list[tuple[int, int]]) -> float:
    # clean up the map
    cmap = copy.deepcopy(dmap)
    for i in range(len(dmap)):
        for j in range(len(dmap[i])):
            point = (j, i)
            if point not in visited:
                cmap[i][j] = "."

    # flood fill to the east and to the south by 1
    newlen = len(cmap) * 2
    bmap: list[list[str]] = [[] for _ in range(newlen)]
    for i in range(0, newlen, 2):
        bmap[i] = ["."] * (len(cmap[0]) * 2)
        bmap[i + 1] = ["."] * (len(cmap[0]) * 2)
        for j in range(0, len(cmap[0]) * 2, 2):
            cmap_indices = (i // 2, j // 2)
            char = cmap[cmap_indices[0]][cmap_indices[1]]
            bmap[i][j] = char
            if char in ("F", "L", "-"):
                bmap[i][j + 1] = "-"
            if char in ("F", "7", "|"):
                bmap[i + 1][j] = "|"
            if char == "S":
                if cmap[cmap_indices[0] + 1][cmap_indices[1]] != ".":
                    bmap[i + 1][j] = "|"
                if cmap[cmap_indices[0]][cmap_indices[1] + 1] != ".":
                    bmap[i][j + 1] = "-"

    # traverse the outside points and fill them in
    outside_points: list[tuple[int, int]] = [(len(bmap[0]) - 1, 0)]
    while outside_points:
        point = outside_points.pop()
        if bmap[point[1]][point[0]] == ".":
            bmap[point[1]][point[0]] = "#"
            if point[0] > 0:
                outside_points.append((point[0] - 1, point[1]))
            if point[0] < len(bmap[0]) - 1:
                outside_points.append((point[0] + 1, point[1]))
            if point[1] > 0:
                outside_points.append((point[0], point[1] - 1))
            if point[1] < len(bmap) - 1:
                outside_points.append((point[0], point[1] + 1))

    # uncomment to visualize
    # with open("output.txt", "w") as f:
    #     for row in bmap:
    #         f.write("".join(row) + "\n")

    # Now let's shrink it back down
    shrink_map = []
    for i, row in enumerate(bmap):
        if i % 2 == 0:
            shrink_map.append([])
        else:
            continue
        for j, char in enumerate(row):
            if j % 2 == 0:
                shrink_map[-1].append(char)

    # uncomment to visualize
    # with open("shrinkput.txt", "w") as f:
    #     for row in shrink_map:
    #         f.write("".join(row) + "\n")

    # count the number of open spaces
    result = 0
    for row in shrink_map:
        for char in row:
            if char == ".":
                result += 1

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input>")
        sys.exit(1)

    data = load(sys.argv[1])
    longway, visited = part1(data)
    print(longway)
    print(part2(data[0], visited))
