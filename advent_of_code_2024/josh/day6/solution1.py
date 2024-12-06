from typing import List

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

pos = [-1, -1]
for r in range(len(room)):
    for c in range(len(room[0])):
        if room[r][c] == '^':
            pos = [r, c]
            break
    if pos[0] != -1:
        break

direction = [-1, 0]


while is_on_board(pos):
    room[pos[0]][pos[1]] = "X"
    next = translate_vector(pos, direction)
    while is_on_board(next) and room[next[0]][next[1]] == "#":
        direction = rotate_vector(direction)
        next = translate_vector(pos, direction)

    pos = next

visited = 0
for r in room:
    visited += r.count("X")

print(visited)