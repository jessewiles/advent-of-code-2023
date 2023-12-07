import dataclasses
import math
import sys


@dataclasses.dataclass
class Race:
    duration: int
    best: int


def parse_input(path: str) -> list[Race]:
    races: list[Race] = []
    with open(path) as f:
        first_line = [n for n in f.readline().strip().split(" ")[1:] if n != ""]
        second_line = [n for n in f.readline().strip().split(" ")[1:] if n != ""]
    for i in range(len(first_line)):
        races.append(Race(duration=int(first_line[i]), best=int(second_line[i])))

    return races


def parse_input_2(path: str) -> list[Race]:
    races: list[Race] = []
    with open(path) as f:
        first_line = [n for n in f.readline().strip().split(" ")[1:] if n != ""]
        second_line = [n for n in f.readline().strip().split(" ")[1:] if n != ""]
    races.append(
        Race(duration=int("".join(first_line)), best=int("".join(second_line)))
    )

    return races


def calculate_race(race: Race) -> list[int]:
    result = []
    for i in range(1, race.duration):
        result.append(i * (race.duration - i))
    return result


def both_parts(races: list[Race]):
    results = []
    for race in races:
        race_results = calculate_race(race)
        results.append([n for n in race_results if n > race.best])

    return math.prod([len(n) for n in results])


if __name__ == "__main__":
    races = parse_input(sys.argv[1])
    print(both_parts(races))
    races = parse_input_2(sys.argv[1])
    print(both_parts(races))
