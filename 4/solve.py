from collections import defaultdict
from functools import reduce


def part1():
    with open("test.txt") as f:
        data = f.read().splitlines()
        winnings = []
        for line in data:
            winners, mine = line.split(": ")[-1].split(" | ")
            winners = set(int(i) for i in winners.split() if i != str())
            mine = set(int(i) for i in mine.split() if i != str())
            my_winners = winners.intersection(mine)
            if my_winners:
                if len(my_winners) == 1:
                    winnings.append(1)
                else:
                    winnings.append(2 ** (len(my_winners) - 1))

        print(sum(winnings))


def part2():
    with open("test2.txt") as f:
        data = f.read().splitlines()
        copies = defaultdict(int)
        for line in data:
            card_parts = line.split(": ")
            card_num = int(card_parts[0].split()[1])
            next_card = card_num + 1

            winners, mine = card_parts[-1].split(" | ")
            winners = set(int(i) for i in winners.split() if i != str())
            mine = set(int(i) for i in mine.split() if i != str())

            my_matches = winners.intersection(mine)
            next_cards_to_copy = range(next_card, next_card + len(my_matches))

            number_of_copies = copies[card_num] + 1

            for cnum in next_cards_to_copy:
                copies[cnum] += number_of_copies

        print(len(copies) + reduce(lambda x, y: x + y, copies.values()))


if __name__ == "__main__":
    part1()
    part2()
