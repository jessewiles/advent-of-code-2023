import collections
import sys


class Hand1:
    _MAP = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }

    def __init__(self, cards: list):
        self.raw = cards[0]
        self.cards = [self._MAP[c] for c in cards[0]]
        self.rank = collections.Counter(self.cards).most_common()
        self.bid = int(cards[1])

    def __repr__(self):
        return f"{self.cards} {self.rank} {self.bid}"

    def hand_is_higher_by_card(self, other: "Hand1") -> bool:
        idx = 0
        while True:
            if self.cards[idx] == other.cards[idx]:
                idx += 1
            else:
                return self.cards[idx] < other.cards[idx]
            if idx == 5:
                return False

    def __lt__(self, other):
        idx = 0
        result = False
        found_order = False
        while idx < len(self.rank) and idx < len(other.rank):
            if self.rank[idx][1] == other.rank[idx][1]:
                idx += 1
            else:
                found_order = True
                result = self.rank[idx][1] < other.rank[idx][1]
                break

        if not found_order:
            result = self.hand_is_higher_by_card(other)

        return result


class Hand2(Hand1):
    _MAP = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
        "J": 1,
    }
    REV_MAP = {
        14: "A",
        13: "K",
        12: "Q",
        10: "T",
        9: "9",
        8: "8",
        7: "7",
        6: "6",
        5: "5",
        4: "4",
        3: "3",
        2: "2",
        1: "J",
    }

    def __init__(self, cards: list):
        self.raw = cards[0]
        self.cards = [self._MAP[c] for c in cards[0]]
        self.rank = collections.Counter(self.cards).most_common()
        self.bid = int(cards[1])
        self.fake = None

        if "J" in self.raw:
            if self.raw == "JJJJJ":
                replacement = "J"
            else:
                try:
                    replacement = [
                        self.REV_MAP[self.rank[t][0]]
                        for t in range(len(self.rank))
                        if self.REV_MAP[self.rank[t][0]] != "J"
                    ][0]
                except IndexError:
                    raise Exception(self.raw, self.rank)
            self.fake = self.raw.replace("J", replacement)
            fake_cards = [self._MAP[c] for c in self.fake]
            self.rank = collections.Counter(fake_cards).most_common()

    def __lt__(self, other):
        idx = 0
        result = False
        found_order = False
        while idx < len(self.rank) and idx < len(other.rank):
            if self.rank[idx][1] == other.rank[idx][1]:
                idx += 1
            else:
                found_order = True
                result = self.rank[idx][1] < other.rank[idx][1]
                break

        if not found_order:
            result = self.hand_is_higher_by_card(other)

        return result


def load(path: str) -> list:
    with open(path, "r") as f:
        return [Hand1(item.split(" ")) for item in f.read().splitlines()]


def load2(path: str) -> list:
    with open(path, "r") as f:
        return [Hand2(item.split(" ")) for item in f.read().splitlines()]


def part1(data: list):
    sorted_data = sorted(data)
    sorts = [((i + 1) * x.bid) for i, x in enumerate(sorted_data)]
    return sum(sorts)


def part2(data: list):
    sorted_data = sorted(data)
    sorts = [((i + 1) * x.bid) for i, x in enumerate(sorted_data)]
    return sum(sorts)


if __name__ == "__main__":
    data = load(sys.argv[1])
    print(part1(data))
    data = load2(sys.argv[1])
    print(part2(data))
