import re

memory = open("./advent_of_code_2024/josh/day3/input.txt").read()

matches = re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", memory)

ignore = False
sum = 0

# For part 1, just change line 13 to ignore = False so we never ignore.
for idx, match in enumerate(matches):
    if match == "don't()":
        ignore = True
    elif match == "do()":
        ignore = False
    else:
        if not ignore:
            nums = re.findall(r"\d+", match)
            sum += int(nums[0]) * int(nums[1])

print(sum)
