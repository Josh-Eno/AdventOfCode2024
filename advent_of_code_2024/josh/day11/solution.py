from collections import defaultdict
from functools import reduce
from typing import Dict, List
import time

# Next map stores a list of next elements for a given element
step_map: Dict[str, List[str]] = {}

# Lookup serves the dual purpose of populating the step_map, and retrieving entries we've seen.
# An alternative would've been to use the python @cache annotation from functools, but I wanted to 
# see it myself.
def lookup(element: str) -> List[str]:
    if element in step_map:
        return step_map[element]
    if element == "0":
        step_map[element] = ["1"]
        return ["1"]
    if len(element) % 2 == 0:
        middle = int(len(element) / 2)
        split = [str(int(element[:middle])), str(int(element[middle:]))]
        step_map[element] = split
        return split
    
    next = [str(int(element) * 2024)]
    step_map[element] = next
    return next
    
def blink(token_counts: Dict[str, int]) -> Dict[str, int]:
    new_counts = defaultdict(int)

    for token, count in token_counts.items():
        next_tokens = lookup(token)
        for next in next_tokens:
            new_counts[next] += count

    return new_counts
    
input = open("./advent_of_code_2024/josh/day11/input.txt").read().strip()
# input = "125 17"

stones = input.split()
token_counts = defaultdict(int)
for stone in stones:
    token_counts[stone] += 1

for i in range(75):
    token_counts = blink(token_counts)

sum = 0
for count in token_counts.values():
    sum += count

print(f"Map has {sum} entries")
