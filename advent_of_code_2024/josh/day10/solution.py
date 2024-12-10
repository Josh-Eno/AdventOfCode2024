from typing import Dict, List

class Waypoint:
    def __init__(self, row: int, col: int, height: int, dim: int):
        self.row = row
        self.col = col
        self.height = height
        self.exits: List['Waypoint'] = []
        self.adjacents = []
        self.trail_count = 0
        self.trail_rating = 0

        if row > 0:
            self.adjacents.append((row - 1, col))
        if col > 0:
            self.adjacents.append((row, col - 1))
        if row < dim - 1:
            self.adjacents.append((row + 1, col))
        if col < dim - 1:
            self.adjacents.append((row, col + 1))
        
    def to_str(self)-> str:
        return f"({self.row}, {self.col}): {self.height}"
    def add_exits(self, directory: Dict[tuple, 'Waypoint']):
        for adjacent in self.adjacents:
            if directory[adjacent].height == self.height + 1:
                self.exits.append(directory[adjacent])

    def count_trails(self, part_two: bool = False) -> int:
        if self.height != 0:
            return 0
        frontier = self.exits
        next_frontier: List['Waypoint'] = [] 
        while frontier and frontier[0].height != 9:
            for waypoint in frontier:
                next_frontier.extend(waypoint.exits)
            frontier = next_frontier
            next_frontier = []
        
        self.trail_count = len(set(frontier))
        self.trail_rating = len(frontier)

        return self.trail_count

input = [
    "89010123",
    "78121874",
    "87430965",
    "96549874",
    "45678903",
    "32019012",
    "01329801",
    "10456732"
]
input = open("./advent_of_code_2024/josh/day10/input.txt").read().splitlines()

dim = len(input)
directory: Dict[tuple, Waypoint] = {}
trailheads = []
for r in range(dim):
    for c in range(dim):
        wp = Waypoint(r, c, int(input[r][c]), dim)
        directory[(r, c)] = wp
        if wp.height == 0:
            trailheads.append(wp)

for waypoint in directory.values():
    waypoint.add_exits(directory)

trails = 0
rating = 0
for wp in trailheads:
    trails += wp.count_trails()
    rating += wp.trail_rating

print(f"Total trails: {trails}")
print(f"Total rating: {rating}")
