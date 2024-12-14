from collections import defaultdict
import re
from typing import List

class Robot:

    def __init__(self, line: str, x_dim: int, y_dim: int):
        parts = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)
        self.x = int(parts.group(1))
        self.y = int(parts.group(2))
        self.dx = int(parts.group(3))
        self.dy = int(parts.group(4))
        self.x_dim = x_dim
        self.y_dim = y_dim

    def __str__(self):
        return "p=({},{}) v=({},{})".format(self.x, self.y, self.dx, self.dy)

    def move(self, turns: int):
        x_dest_raw = (self.x + self.dx * turns) % self.x_dim
        y_dest_raw = (self.y + self.dy * turns) % self.y_dim
        self.x = x_dest_raw if x_dest_raw >= 0 else self.x_dim - x_dest_raw
        self.y = y_dest_raw if y_dest_raw >= 0 else self.y_dim - y_dest_raw
    
    def get_quadrant(self):
        x_axis = int(self.x_dim / 2)
        y_axis = int(self.y_dim / 2)
        if self.x == x_axis or self.y == y_axis:
            return 0

        if self.x > self.x_dim / 2:
            if self.y > self.y_dim / 2:
                return 4
            elif self.y < self.y_dim / 2:
                return 1
        else:
            if self.y > self.y_dim / 2:
                return 3
            elif self.y < self.y_dim / 2:
                return 2

def render(robots: List[Robot], x_dim: int, y_dim: int) -> str:
    grid = [["." for _ in range(x_dim)] for _ in range(y_dim)]
    
    for robot in robots:
        grid[robot.y][robot.x] = "#"

    string = ""
    for row in grid:
        string += "".join(row) + "\n"
    
    return string

x_dim = 11
y_dim = 7
input = [
    "p=0,4 v=3,-3",
    "p=6,3 v=-1,-3",
    "p=10,3 v=-1,2",
    "p=2,0 v=2,-1",
    "p=0,0 v=1,3",
    "p=3,0 v=-2,-2",
    "p=7,6 v=-1,-3",
    "p=3,0 v=-1,-2",
    "p=9,3 v=2,3",
    "p=7,3 v=-1,2",
    "p=2,4 v=2,-3",
    "p=9,5 v=-3,-3"
]

x_dim = 101
y_dim = 103
input = open("./advent_of_code_2024/josh/day14/input.txt").read().splitlines()

robots: List[Robot] = []

for line in input:
    robot = Robot(line, x_dim, y_dim)
    robots.append(robot)

# Part 1:
part_1 = False
if part_1:
    quad_cnt = defaultdict(int)

    for robot in robots:
        robot.move(100)
        quad_cnt[robot.get_quadrant()] += 1

    score = 1
    for q in range(1,5):
        score *= quad_cnt[q]

    print(score)

# part 2:
regex = re.compile(r"#{8,}")
output = open("./advent_of_code_2024/josh/day14/output.txt", "w")
for i in range(10000):
    for robot in robots:
        robot.move(1)
    state = render(robots, x_dim, y_dim)
    matches = len(regex.findall(state))
    if matches > 1:
        output.write(f"moves: {i + 1} \n")
        output.write(state + "\n\n")
        print(state)

