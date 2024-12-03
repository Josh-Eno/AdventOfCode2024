list_lines = open("./advent_of_code/src/josh/day1a/input.txt").read().splitlines()

# Split lines, delimited by '   '
split_lines = [x.split("   ") for x in list_lines]

list1 = [int(x[0]) for x in split_lines] 
list2 = [int(x[1]) for x in split_lines]

list1.sort()
list2.sort()
diff = 0

for idx in range(len(list1)):
    diff += abs(list1[idx] - list2[idx])

print(diff)
