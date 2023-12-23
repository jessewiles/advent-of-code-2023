import dataclasses
import itertools
import pprint
import sys


@dataclasses.dataclass
class Galaxy:
    location: tuple[int, int]


class Universe:
    def __init__(self, data: list, galaxy_locations: dict[str, tuple[int, int]]):
        self.data = data
        self.galaxy_locations = galaxy_locations
        self.galaxy_count = len(galaxy_locations.keys())
        self.galaxy_map: dict[str, Galaxy] = {}
        self.expanded: list[list[str]] = []

    def expand(self, factor: int = 1) -> dict[str, tuple[int, int]]:
        set_of_columns = set(x[0] for x in self.galaxy_locations.values())
        set_of_rows = set(x[1] for x in self.galaxy_locations.values())
        expansion_colunms = [
            i for i in range(len(self.data[0])) if i not in set_of_columns
        ]
        expansion_rows = [i for i in range(len(self.data)) if i not in set_of_rows]

        updated_galaxy_locations: dict[str, tuple[int, int]] = {}
        for galaxy_id, location in self.galaxy_locations.items():
            updated_galaxy_locations[galaxy_id] = (
                location[0]
                + len([i for i in expansion_colunms if i < location[0]]) * (factor - 1),
                location[1]
                + len([i for i in expansion_rows if i < location[1]]) * (factor - 1),
            )

        """
        # This doesn't work, for extremely large values. Only helpful for debugging
        from pprint import pprint
        pprint(updated_galaxy_locations)
        self.expanded = [
            ["."] * (len(self.data[0]) + len(expansion_colunms) * factor)
            for _ in range(len(self.data) + len(expansion_rows) * factor)
        ]
        print(len(self.expanded), len(self.expanded[0]))
        for galaxy_id, location in updated_galaxy_locations.items():
            self.expanded[location[1]][location[0]] = galaxy_id

        with open("expanded.txt", "w") as f:
            for line in self.expanded:
                f.write("".join(line) + "\n")
        """

        return updated_galaxy_locations


def load_data(filename: str) -> Universe:
    data = []
    galaxy_count = 1
    line_count = 0
    galaxy_locations: dict[str, tuple[int, int]] = {}
    for line in open(filename, "r"):
        line_list = list(line.strip())
        for i in range(len(line_list)):
            if line_list[i] == "#":
                gc = str(galaxy_count)
                line_list[i] = gc
                galaxy_locations[gc] = (i, line_count)
                galaxy_count += 1
        data.append(line_list)
        line_count += 1
    uni = Universe(data, galaxy_locations)
    return uni


def part1(uni: Universe) -> int:
    updated = uni.expand()
    combos = itertools.combinations(range(1, len(updated) + 1), 2)
    distances = []
    for combo in combos:
        galaxy1 = updated[str(combo[0])]
        galaxy2 = updated[str(combo[1])]
        distance = abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])
        distances.append(distance)

    return sum(distances)


def part2(uni: Universe) -> int:
    updated = uni.expand(factor=1_000_000)
    combos = itertools.combinations(range(1, len(updated) + 1), 2)
    distances = []
    for combo in combos:
        galaxy1 = updated[str(combo[0])]
        galaxy2 = updated[str(combo[1])]
        distance = abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])
        distances.append(distance)

    return sum(distances)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python solve.py <input file>")
        sys.exit(1)
    data = load_data(sys.argv[1])
    print(part1(data))
    print(part2(data))
