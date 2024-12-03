import re

hardPattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|(don't\(\))|(do\(\))")
easyPattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

with open('input.txt', 'r') as file:
    lines = file.readlines()
    input = ''.join(lines)

easyGroups = re.findall(easyPattern, input)
hardGroups = re.findall(hardPattern, input)

# Solution 1
easyTotal = 0
for group in easyGroups:
    easyTotal += int(group[0]) * int(group[1])

# Solution 2
hardTotal = 0
do = True
for group in hardGroups:
    if group[2] == "don't()":
        do = False
    elif group[3] == "do()":
        do = True
    else:
        if do:
            hardTotal += int(group[0]) * int(group[1])


print("Problem 1: " + str(easyTotal))
print("Problem 2: " + str(hardTotal))
