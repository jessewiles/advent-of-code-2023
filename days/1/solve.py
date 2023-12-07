NUMBER_WORDS_FORWARD = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
PARTIAL_FORWARD = set()
for i in NUMBER_WORDS_FORWARD.keys():
    max_len = len(i) - 1
    for j in range(max_len):
        PARTIAL_FORWARD.add(i[: j + 1])

NUMBER_WORDS_BACKWARD = {
    "eno": "1",
    "owt": "2",
    "eerht": "3",
    "ruof": "4",
    "evif": "5",
    "xis": "6",
    "neves": "7",
    "thgie": "8",
    "enin": "9",
}
PARTIAL_BACKWARD = set()
for i in NUMBER_WORDS_BACKWARD.keys():
    max_len = len(i) - 1
    for j in range(max_len):
        PARTIAL_BACKWARD.add(i[: j + 1])


def part1():
    with open("test.txt", "r") as reader:
        totals = []
        for line in reader.readlines():
            nums = []
            for char in line:
                if char.isnumeric():
                    nums.append(char)
            totals.append(int("".join([nums[0], nums[-1]])))
        print(sum(totals))


def part2():
    with open("test.txt", "r") as reader:
        totals = []
        for line in reader.readlines():
            front_word = str()
            back_word = str()
            front_num = str()
            back_num = str()
            cline = line.strip().lower()

            for idx in range(len(cline)):
                if front_num and back_num:
                    break

                if not front_num:
                    front_char = cline[idx]
                    if front_char.isalpha():
                        front_word += front_char
                        if front_word in NUMBER_WORDS_FORWARD:
                            front_num = NUMBER_WORDS_FORWARD[front_word]
                        elif front_word not in PARTIAL_FORWARD:
                            while front_word:
                                front_word = front_word[1:]
                                if front_word in PARTIAL_FORWARD:
                                    break
                    elif front_char.isnumeric():
                        front_num = front_char
                    else:
                        raise Exception("WTF: %s" % front_char)

                if not back_num:
                    back_char = cline[-idx - 1]
                    if back_char.isalpha():
                        back_word += back_char
                        if back_word in NUMBER_WORDS_BACKWARD:
                            back_num = NUMBER_WORDS_BACKWARD[back_word]
                        elif back_word not in PARTIAL_BACKWARD:
                            while back_word:
                                back_word = back_word[1:]
                                if back_word in PARTIAL_BACKWARD:
                                    break
                    elif back_char.isnumeric():
                        back_num = back_char
                    else:
                        raise Exception("WTF: %s" % back_char)

            totals.append(int("".join([front_num, back_num])))
        print(sum(totals))


if __name__ == "__main__":
    part1()
    part2()
