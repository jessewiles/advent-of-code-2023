from collections import defaultdict
from functools import reduce

MAXES = {"red": 12, "green": 13, "blue": 14}


def part1():
    with open("test.txt", "r") as f:
        total = []
        lines = f.readlines()
        for line in lines:
            good_game = True
            rgame, _, rclues = line.partition(":")
            game = int(rgame.replace("Game ", str()))
            tries = rclues.split(";")
            for atry in tries:
                clues = atry.strip().split(", ")
                for clue in clues:
                    rnumber, _, color = clue.partition(" ")
                    number = int(rnumber)

                    if number > MAXES[color]:
                        good_game = False
                        break
            if good_game:
                total.append(game)

        print(sum(total))


# part 2
def part2():
    with open("test.txt", "r") as f:
        total = []
        lines = f.readlines()
        for line in lines:
            game_mins = defaultdict(list)
            _, _, rclues = line.partition(":")
            tries = rclues.split(";")
            for atry in tries:
                clues = atry.strip().split(", ")
                for clue in clues:
                    rnumber, _, color = clue.partition(" ")
                    number = int(rnumber)
                    game_mins[color].append(number)
            total.append(reduce(lambda x, y: x * max(y), game_mins.values(), 1))
        print(sum(total))


if __name__ == "__main__":
    part1()
    part2()
