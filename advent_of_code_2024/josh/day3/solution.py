import re

memory = open("./advent_of_code_2024/josh/day3/input.txt").read()

# Finds patterns "mul(<int>,<int>)", "do()", and "don't()"
matches = re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", memory)

# Change to True for part 2
is_part2 = False
ignore = False
sum = 0

for match in matches:
    if match == "don't()":
        ignore = is_part2
    elif match == "do()":
        ignore = False
    else:
        if not ignore:
            nums = re.findall(r"\d+", match)
            sum += int(nums[0]) * int(nums[1])

print(sum)
