from typing import List

def check_for_cross(r: int, c: int, input: List[str]) -> bool:
    if (
        ((input[r-1][c-1] == "M" and input[r+1][c+1] == "S") or (input[r-1][c-1] == "S" and input[r+1][c+1] == "M")) and 
        ((input[r-1][c+1] == "M" and input[r+1][c-1] == "S") or (input[r-1][c+1] == "S" and input[r+1][c-1] == "M"))
    ):
        return True
    return False

input = open("./advent_of_code_2024/josh/day4/input.txt").read().strip().split("\n")
rows = len(input)
cols = len(input[0])
cross_count = 0

for r in range(1, rows - 1):
    for c in range(1, cols - 1):
        if input[r][c] == "A":
            if check_for_cross(r, c, input):
                cross_count += 1

print(cross_count)
