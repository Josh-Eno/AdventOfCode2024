from collections import defaultdict
from typing import Dict, List, Set


def is_valid(line: List[str], appears_before: Dict[str, Set[str]]):
    line_set = set(line)

    for elem in line:
        line_set.remove(elem)
        if elem in appears_before and (appears_before[elem] & line_set):
            return False
    return True

def ordered_intersection(line: List[str], set: Set[str]) -> List[str]:
    intersection = []
    for elem in line:
        if elem in set:
            intersection.append(elem)
    
    return intersection

def validate(line: List[str], appears_before: Dict[str, Set[str]]) -> str:
    if is_valid(line, appears_before):
        print("already valid!")
        return line

    valid = []
    working = line.copy()
    while len(valid) < len(line):
        elem = working[0]
        out_of_order = ordered_intersection(working, appears_before[elem])
        if out_of_order:
            for ooo in out_of_order:
                ooo_count = working.count(ooo)
                working.remove(ooo)
                for _ in range(ooo_count):
                    working.insert(0, ooo)
        else:
            working.pop(0)
            valid.append(elem)

    # Sanity check
    if not is_valid(valid, appears_before):
        raise Exception("Invalid sequence!")
    
    return valid


input = open("./advent_of_code_2024/josh/day5/input.txt").read().strip().split("\n")

appears_before = defaultdict(set)
sequences = []

for line in input:
    if line == "":
        continue
    parts = line.split("|")
    if len(parts) > 1:
        # create a map of numbers that must always appear before a given number
        appears_before[parts[1]].add(parts[0])
    else:
        sequences.append(line.split(","))
    
# Now iterate through each line to check/fix validity
sum_1 = 0
sum_2 = 0
for seq in sequences:
    if is_valid(seq, appears_before):
        sum_1 += int(seq[int(len(seq)/2)])
    else:
        valid = validate(seq, appears_before)
        sum_2 += int(valid[int(len(seq)/2)])
        

print(sum_1)
print(sum_2)