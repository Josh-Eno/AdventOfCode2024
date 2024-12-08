from collections import defaultdict
from typing import List, Optional, Set

class Solution:

    def __init__(self, input: List[str], part_2: bool = False):
        self.input = input
        self.nodes = set()
        self.max_r = len(input) - 1
        self.max_c = len(input[0]) - 1
        self.part_2 = part_2

        self.antenna_map = defaultdict(list)

        for r in range(self.max_r + 1):
            for c in range(self.max_c + 1):
                if input[r][c] != ".":
                    self.antenna_map[input[r][c]].append((r, c))
                    if self.part_2:
                        self.nodes.add((r, c))

    def valid_node(self, node: tuple) -> bool:
        return (
            node[0] >= 0 and 
            node[1] >= 0 and 
            node[0] <= self.max_r and 
            node[1] <= self.max_c
        )

    def compute_nodes(self) -> Set[tuple]:
        for antennas in self.antenna_map.values():
            self.nodes = self.nodes.union(self.get_nodes(antennas))

        return self.nodes

    def compute_next(self, base: tuple, diff: tuple) -> Optional[tuple]:
        next = (base[0] + diff[0], base[1] + diff[1])
        if self.valid_node(next):
            return next
        return None

    def get_nodes(self, antennas: List[tuple]) -> Set[tuple]:
        nodes = set()

        for i in range(len(antennas)):
            for j in range(i + 1, len(antennas)):
                diff = (antennas[j][0] - antennas[i][0], antennas[j][1] - antennas[i][1])
                neg_diff = (-diff[0], -diff[1])
                # Check subtracting
                next = self.compute_next(antennas[i], neg_diff)
                while next:
                    nodes.add(next)
                    next = self.compute_next(next, neg_diff) if self.part_2 else None

                # Check adding
                next = self.compute_next(antennas[j], diff)
                while next:
                    nodes.add(next)
                    next = self.compute_next(next, diff) if self.part_2 else None
    
        return nodes

input = [
    "............",
    "........0...",
    ".....0......",
    ".......0....",
    "....0.......",
    "......A.....",
    "............",
    "............",
    "........A...",
    ".........A..",
    "............",
    "............",
]
input = open("./advent_of_code_2024/josh/day8/input.txt").read().strip().split("\n")

solution = Solution(input, True)
nodes = solution.compute_nodes()

print(f" Total antinodes: {len(nodes)}")