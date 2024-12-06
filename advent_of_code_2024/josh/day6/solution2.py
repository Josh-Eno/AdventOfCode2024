from copy import deepcopy
from typing import List
import time

transition_matrix = [[0, 1], -1, 0]

def rotate_vector(vector: List[str]) -> List[str]:
    return [
        transition_matrix[0][0] * vector[0] + transition_matrix[0][1] * vector[1],
        transition_matrix[1] * vector[0] + transition_matrix[2] * vector[1]
    ]

def translate_vector(vector: List[str], translation: List[str]) -> List[str]:
    return [
        vector[0] + translation[0],
        vector[1] + translation[1]
    ]

def is_on_board(vector: List[str]) -> bool:
    return vector[0] >= 0 and vector[0] < len(room) and vector[1] >= 0 and vector[1] < len(room[0])

def has_cycle(start: List[str], direction: List[str], room: List[List[str]]) -> bool:
    steps = 0
    room_size = len(room) * len(room[0])
    pos = start.copy()
    next = translate_vector(pos, direction)

    while is_on_board(pos) and steps < room_size:
        next = translate_vector(pos, direction)
    
        while is_on_board(next) and room[next[0]][next[1]] == "#":
            direction = rotate_vector(direction)
            next = translate_vector(pos, direction)

        pos = next
        steps += 1

    return is_on_board(pos)

input = [
    "....#.....",
    ".........#",
    "..........",
    "..#.......",
    ".......#..",
    "..........",
    ".#..^.....",
    "........#.",
    "#.........",
    "......#..."
]
input = open("./advent_of_code_2024/josh/day6/input.txt").read().strip().split("\n")

room = list(map(list, input))

start = [-1, -1]
for r in range(len(room)):
    for c in range(len(room[0])):
        if room[r][c] == '^':
            start = [r, c]
            break
    if start[0] != -1:
        break

start_dir = [-1, 0]
cycles = 0

start_time = time.time()

for r in range(len(room)):
    for c in range(len(room[0])):
        if room[r][c] != '^' and room[r][c] != '#':
            test = deepcopy(room)
            test[r][c] = '#'    
            if has_cycle(start, start_dir, test):
                cycles += 1

end_time = time.time()
length = end_time - start_time
print(f"Found {cycles} in {length} seconds.")