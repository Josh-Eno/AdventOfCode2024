import re
from typing import List

class Day4:

    def __init__(self):
        self.input = open("./advent_of_code_2024/josh/day4/input.txt").read().strip().split("\n")
        self.pattern = part1_pattern = re.compile(r"XMAS")
        self.rows = len(self.input)
        self.cols = len(self.input[0])
        self.strings = self.input.copy()
        for string in self.input:
            self.strings.append(string[::-1])

    def get_columns(self):
        columns = []
        for i in range(self.cols):
            column = ""
            for j in range(self.rows):
                column += self.input[j][i]
            columns.append(column)
            columns.append(column[::-1])
        return columns

    def get_diagonal(self, start_row: int, start_col: int, slope: int) -> str:
        diag = ""
        r = start_row
        c = start_col
        while 0 <= r < self.rows and 0 <= c < self.cols:
            diag += self.input[r][c]
            r += 1 * slope
            c += 1 

        return diag

    def get_neg_slope_diagonals(self) -> List[str]:
        diags = []
        for r in range(self.rows):
            diag = self.get_diagonal(r, 0, 1)
            diags.extend([diag, diag[::-1]])
        for c in range(1, self.cols):
            diag = self.get_diagonal(0, c, 1)
            diags.extend([diag, diag[::-1]])

        return diags

    def get_pos_slope_diagonals(self) -> List[str]:
        diags = []
        for r in range(self.rows):
            diag = self.get_diagonal(r, 0, -1)
            diags.extend([diag, diag[::-1]])
        for c in range(1, self.cols):
            diag = self.get_diagonal(self.rows-1, c, -1)
            diags.extend([diag, diag[::-1]])

        return diags

    def print_strings(self, strings: List[str]):
        for string in strings:
            print(string)

    def solve(self):
        self.strings.extend(self.get_columns())
        self.strings.extend(self.get_neg_slope_diagonals())
        self.strings.extend(self.get_pos_slope_diagonals())
        full_str = ".".join(self.strings)
        print(len(list(self.pattern.findall(full_str))))

solution = Day4()
solution.solve()