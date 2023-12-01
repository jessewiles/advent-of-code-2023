with open("input.txt", "r") as reader:
    totals = []
    for line in reader.readlines():
        nums = []
        for char in line:
            if char.isnumeric():
                nums.append(char)
        totals.append(int("".join([nums[0], nums[-1]])))
    print(sum(totals))
