import numpy as np
from typing import List
import re

class System:
    def __init__(self, lines: List[str]):
        a_x, a_y = re.search(r"X.(\d+), Y.(\d+)", lines[0]).groups()
        b_x, b_y = re.search(r"X.(\d+), Y.(\d+)", lines[1]).groups()
        c_x, c_y = re.search(r"X.(\d+), Y.(\d+)", lines[2]).groups()

        self.is_valid = False
        self.cramers_valid = False
        self.mat: List[List[np.double]] = [[np.double(a_x), np.double(b_x)], [np.double(a_y), np.double(b_y)]]
        self.y_vec = [[np.double(c_x) + 10000000000000], [np.double(c_y) + 10000000000000]]
        self.invert_mat()
        self.solution = []
        self.solve()

    def to_str(self) -> str:
        return f"matrix: {self.mat} \ninverse: {self.inverse} \ntarget: {self.y_vec} \nsolution: {self.solution}\n \nvalid: {self.is_valid}"

    def invert_mat(self):
        self.det_factor = (self.mat[0][0] * self.mat[1][1]) - (self.mat[0][1] * self.mat[1][0])
        if self.det_factor == 0:
            self.det_factor = -1
            self.inverse = None

        self.inverse = [
            [int(self.mat[1][1]), -int(self.mat[0][1])],
            [-int(self.mat[1][0]), int(self.mat[0][0])]
        ]

    def solve(self):
        if self.det_factor == -1:
            self.solution = None
            self.is_valid = False
            return

        self.solution = [
            [(self.inverse[0][0] * self.y_vec[0][0]) / self.det_factor + (self.inverse[0][1] * self.y_vec[1][0]) / self.det_factor],
            [(self.inverse[1][0] * self.y_vec[0][0]) / self.det_factor + (self.inverse[1][1] * self.y_vec[1][0]) / self.det_factor]
        ]

        # Check if we have integer coefficients
        if (abs(self.solution[0][0] - round(self.solution[0][0])) < 0.0001 and 
            abs(self.solution[1][0] - round(self.solution[1][0])) < .0001):
            self.is_valid = True
            self.solution = [round(self.solution[0][0]), round(self.solution[1][0])]
    
input = [
    "Button A: X+94, Y+34",
    "Button B: X+22, Y+67",
    "Prize: X=8400, Y=5400",
    "",
    "Button A: X+26, Y+66",
    "Button B: X+67, Y+21",
    "Prize: X=12748, Y=12176",
    "",
    "Button A: X+17, Y+86",
    "Button B: X+84, Y+37",
    "Prize: X=7870, Y=6450",
    "",
    "Button A: X+69, Y+23",
    "Button B: X+27, Y+71",
    "Prize: X=18641, Y=10279",
]
input = open("./advent_of_code_2024/josh/day13/input.txt").read().splitlines()

start_idx = 0
valid_systems = []
invalid_systems = []
total_cost = 0
while start_idx < len(input):
    system = System(input[start_idx:start_idx + 3])
    if system.is_valid:
        valid_systems.append(system)
        total_cost += 3*system.solution[0] + system.solution[1]
    start_idx += 4

print(f"Total cost: {total_cost}")

