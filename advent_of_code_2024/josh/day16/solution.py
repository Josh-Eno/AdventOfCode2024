from heapq import heapify, heappush, heappop 
from typing import Dict, Tuple, List, Set

class PathNode:
    TURN_COST = 1000

    def __init__(self, maze: List[str], location: Tuple[int, int], cost: int, prev_loc: Tuple[int, int]):
        self.prev_loc: Tuple[int, int] = prev_loc
        self.location: Tuple[int, int] = location
        self.cost: int = cost
        self.maze: List[str] = maze
    
    def __eq__(self, other: 'PathNode'):
        return (
            self.prev_loc == other.prev_loc and 
            self.location == other.location
        )

    def __hash__(self):
        return hash((self.prev_loc, self.location))

    def __lt__(self, other: 'PathNode'):
        return self.cost < other.cost
    
    def __str__(self):
        return f"PathNode(location={self.location}, cost={self.cost}, prev_loc={self.prev_loc})"

    def get_val(self, node: Tuple[int, int]) -> str:
        return self.maze[node[0]][node[1]]

    def is_turn(self, next: Tuple[int, int]):
        sdr = self.location[0] - self.prev_loc[0]
        sdc = self.location[1] - self.prev_loc[1]

        ndr = next[0] - self.location[0]
        ndc = next[1] - self.location[1]

        return sdr != ndr or sdc != ndc

    def get_neighbors(self) -> List['PathNode']:
        neighbors = []
        up = (self.location[0] - 1, self.location[1])
        down = (self.location[0] + 1, self.location[1])
        right = (self.location[0], self.location[1] + 1)
        left = (self.location[0], self.location[1] - 1)

        if up != self.prev_loc and (self.get_val(up) == "." or self.get_val(up) == "E"):
            cost = self.cost + 1 if not self.is_turn(up) else self.cost + PathNode.TURN_COST + 1
            neighbors.append(self.__class__(self.maze, up, cost, self.location))
        if down != self.prev_loc and (self.get_val(down) == "." or self.get_val(down) == "E"):
            cost = self.cost + 1 if not self.is_turn(down) else self.cost + PathNode.TURN_COST + 1
            neighbors.append(self.__class__(self.maze, down, cost, self.location))
        if left != self.prev_loc and (self.get_val(left) == "." or self.get_val(left) == "E"):
            cost = self.cost + 1 if not self.is_turn(left) else self.cost + PathNode.TURN_COST + 1
            neighbors.append(self.__class__(self.maze, left, cost, self.location))
        if right != self.prev_loc and (self.get_val(right) == "." or self.get_val(right) == "E"):
            cost = self.cost + 1 if not self.is_turn(right) else self.cost + PathNode.TURN_COST + 1
            neighbors.append(self.__class__(self.maze, right, cost, self.location))
        
        return neighbors

def get_costs(costs: Dict[PathNode, int], loc: Tuple[int, int]) -> List[PathNode]:
    found_costs = []
    possibles = {
        PathNode([], loc, 0, (loc[0] - 1, loc[1])),
        PathNode([], loc, 0, (loc[0] + 1, loc[1])),
        PathNode([], loc, 0, (loc[0], loc[1] - 1)),
        PathNode([], loc, 0, (loc[0], loc[1] + 1))
    }

    for node in costs.keys():
        if node in possibles:
            found_costs.append(node)
    
    return found_costs

def render(grid: List[str], nodes_on_path: Set[Tuple[int, int]]):
    output = open("./advent_of_code_2024/josh/day16/output.txt", "w")
    array_grid = [list(row) for row in grid]

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (r, c) in nodes_on_path:
                array_grid[r][c] = "O"
            else:
                array_grid[r][c] = grid[r][c]
    
    for row in array_grid:
        output.write("".join(row) + "\n")

input_file = open("./advent_of_code_2024/josh/day16/input.txt").read().splitlines()

input_test_1 = [
    "###############",
    "#.......#....E#",
    "#.#.###.#.###.#",
    "#.....#.#...#.#",
    "#.###.#####.#.#",
    "#.#.#.......#.#",
    "#.#.#####.###.#",
    "#...........#.#",
    "###.#.#####.#.#",
    "#...#.....#.#.#",
    "#.#.#.###.#.#.#",
    "#.....#...#.#.#",
    "#.###.#.#.#.#.#",
    "#S..#.....#...#",
    "###############"
]

input_test_2 = [
    "#################",
    "#...#...#...#..E#",
    "#.#.#.#.#.#.#.#.#",
    "#.#.#.#...#...#.#",
    "#.#.#.#.###.#.#.#",
    "#...#.#.#.....#.#",
    "#.#.#.#.#.#####.#",
    "#.#...#.#.#.....#",
    "#.#.#####.#.###.#",
    "#.#.#.......#...#",
    "#.#.###.#####.###",
    "#.#.#...#.....#.#",
    "#.#.#.#####.###.#",
    "#.#.#.........#.#",
    "#.#.#.#########.#",
    "#S#.............#",
    "#################"
]

grid = input_test_1

start = PathNode(grid, (len(grid) - 2, 1), 0, (len(grid) - 2, 0))
best_cost = 1000 * len(grid) * len(grid[0])
seen_costs: Dict[PathNode, int] = {start: 0}
frontier = [start]
heapify(frontier)

# This does a non-restrictive BFS without really tracking paths, to set up all the 
# optimal costs in seen_costs
while frontier:
    node = heappop(frontier)
    for neighbor in node.get_neighbors():
        if neighbor in seen_costs:
            prev_neighbor_cost = seen_costs[neighbor]
            # Check if we've arrived with a lower cost. If we have, update the seen cost and re-queue
            # so we propagate the lower cost forward.
            if prev_neighbor_cost > neighbor.cost:
                seen_costs[neighbor] = neighbor.cost
                heappush(frontier, neighbor)
        else:
            heappush(frontier, neighbor)
            seen_costs[neighbor] = neighbor.cost
    if node.location == (1, len(grid[0]) - 2):
        best_cost = min(best_cost, node.cost)
    
print(f"Best cost: {best_cost}")

# For part 2, do DFS, and return all tuples that are part of a path that gets to E for cost
def dfs(maze: List[str], parents: List[PathNode], cost_limit: int) -> List[PathNode]:
    nodes_on_path = []
    branches = parents[-1].get_neighbors()
    for node in branches:
        # If we find the end, start the recursion
        if node.location == (1, len(maze[0]) - 2):
            if node.cost == cost_limit:
                return[node]
            else:
                return []

        if node not in parents and node.cost <= cost_limit:
            nodes_on_branch = dfs(maze, parents + [node], cost_limit)
            if nodes_on_branch:
                nodes_on_path += nodes_on_branch + [node]
                
    return nodes_on_path

nodes_on_path = set(dfs(grid, [start], best_cost))
print(f"From DFS: {len(nodes_on_path)}")
tuples_on_path = [x.location for x in nodes_on_path]
render(grid, tuples_on_path)
