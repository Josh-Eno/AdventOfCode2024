from collections import defaultdict

list_lines = open("./advent_of_code_2024/josh/day1a/input.txt").read().splitlines()

# Split lines, delimited by '   '
split_lines = [x.split("   ") for x in list_lines]

list1 = [int(x[0]) for x in split_lines] 
list2 = [int(x[1]) for x in split_lines]

counts = defaultdict(int)
for elem in list2:
    counts[elem] += 1

sum = 0

for elem in list1:
    sum += elem * counts[elem] if elem in counts else 0

print(sum)
