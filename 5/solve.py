import concurrent.futures
import math
import sys


ALMANAC_MAPS = {
    "seed-to-soil": [],
    "soil-to-fertilizer": [],
    "fertilizer-to-water": [],
    "water-to-light": [],
    "light-to-temperature": [],
    "temperature-to-humidity": [],
    "humidity-to-location": [],
}

LOOKUP_PATH = {
    "seed-to-soil": "soil-to-fertilizer",
    "soil-to-fertilizer": "fertilizer-to-water",
    "fertilizer-to-water": "water-to-light",
    "water-to-light": "light-to-temperature",
    "light-to-temperature": "temperature-to-humidity",
    "temperature-to-humidity": "humidity-to-location",
    "humidity-to-location": None,
}


def read_almanac(file_path: str):
    with open(file_path) as f:
        line = f.readline().strip()
        seeds = [int(i) for i in line.split(":")[1].strip().split(" ")]

        active_map = None
        for line in f.readlines():
            line = line.strip()
            if line == "":
                continue
            if line[0].isalpha():
                active_map = ALMANAC_MAPS[line[:-5]]
                continue
            elif line[0].isdigit():
                digits = (int(i) for i in line.split(" "))
                destination_start_range, source_start_range, range_length = digits
                if active_map is None:
                    raise ValueError("No active map")
                active_map.append(
                    (
                        source_start_range,
                        destination_start_range,
                        range_length,
                    )
                )
    return seeds


def part1(seeds: list[int]):
    locations = []
    for seed in seeds:
        current = seed
        key = "seed-to-soil"
        # breakpoint()
        while key in LOOKUP_PATH:
            ranges = ALMANAC_MAPS[key]
            for source_start_range, destination_start_range, range_length in ranges:
                if (
                    current >= source_start_range
                    and current < source_start_range + range_length
                ):
                    current = destination_start_range + (current - source_start_range)
                    break
            key = LOOKUP_PATH[key]

        locations.append(current)
    print(min(locations))


def part2(seeds: list[int]):
    def work(seeds, idx) -> int | float:
        winner = math.inf
        start, rlen = seeds[idx], seeds[idx + 1]
        print(f"iteration {idx}...")
        for j in range(rlen):
            current = start + j
            key = "seed-to-soil"
            # breakpoint()
            while key in LOOKUP_PATH:
                ranges = ALMANAC_MAPS[key]
                for source_start_range, destination_start_range, range_length in ranges:
                    if (
                        current >= source_start_range
                        and current < source_start_range + range_length
                    ):
                        current = destination_start_range + (
                            current - source_start_range
                        )
                        break
                key = LOOKUP_PATH[key]

            if current < winner:
                winner = current
        return winner

    # 10 seed ranges
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(work, seeds, i) for i in range(0, len(seeds), 2)]

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
            except Exception as e:
                print(f"Generated an exception: {e}")
            else:
                print(f"Result: {result}")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        raise ValueError("Missing input file")
    seeds = read_almanac(sys.argv[1])
    part1(seeds)
    part2(seeds)
