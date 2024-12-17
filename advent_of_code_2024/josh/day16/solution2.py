from collections import defaultdict
from heapq import heapify, heappush, heappop 
from typing import Dict, Tuple, List, Set

class Path:
    def __init__(self, maze: List[str], edges: List[Tuple[Tuple[int, int], Tuple[int, int]]], cost: int): 
        self.maze = maze
        self.edges = edges
        self.cost = cost

    def is_turn(self, next: Tuple[Tuple[int, int], Tuple[int, int]]):
        end = self.edges[-1]
        sdr = end[1][0] - end[0][0]
        sdc = end[1][1] - end[0][1]

        ndr = next[1][0] - next[0][0]
        ndc = next[1][1] - next[0][1]

        return sdr != ndr or sdc != ndc

    def __lt__(self, other):
        return self.cost < other.cost

    def extend(self) -> List['Path']:
        final_edge = self.edges[-1]
        
        extensions = []
        ext_node = final_edge[1]
        up = (ext_node, (ext_node[0] - 1, ext_node[1]))
        down = (ext_node, (ext_node[0] + 1, ext_node[1]))
        left = (ext_node, (ext_node[0], ext_node[1] - 1))
        right = (ext_node, (ext_node[0], ext_node[1] + 1))
        if self.maze[up[1][0]][up[1][1]] != "#" and up[1] != final_edge[0]:
            is_turn = self.is_turn(up)
            cost = self.cost + 1001 if is_turn else self.cost + 1
            extensions.append(self.__class__(self.maze, self.edges + [up], cost))
        if self.maze[down[1][0]][down[1][1]] != "#" and down[1] != final_edge[0]:
            is_turn = self.is_turn(down)
            cost = self.cost + 1001 if is_turn else self.cost + 1
            extensions.append(self.__class__(self.maze, self.edges + [down], cost))
        if self.maze[left[1][0]][left[1][1]] != "#" and left[1] != final_edge[0]:
            is_turn = self.is_turn(left)
            cost = self.cost + 1001 if is_turn else self.cost + 1
            extensions.append(self.__class__(self.maze, self.edges + [left], cost))
        if self.maze[right[1][0]][right[1][1]] != "#" and right[1] != final_edge[0]:
            is_turn = self.is_turn(right)
            cost = self.cost + 1001 if is_turn else self.cost + 1
            extensions.append(self.__class__(self.maze, self.edges + [right], cost))
        
        return extensions
    
    def copy(self):
        return self.__class__(self.maze, self.edges.copy(), self.cost)

def add_path_nodes(path: Path, max_length: int) -> Set[Tuple[int, int]]:
    node_set = set()
    for idx, edge in enumerate(path.edges):
        if idx == max_length:
            return node_set
        node_set.add(edge[0])
        node_set.add(edge[1])
        other_paths = edge_paths[edge]
        if len(other_paths) > 1:
            for other_path in other_paths:
                if other_path.edges[-2] != path.edges[idx - 1]:
                    node_set.update(add_path_nodes(other_path, len(other_path.edges) - 2))
    
    return node_set

def render(grid: List[str], nodes_on_path: Set[Tuple[int, int]]):
    output = open("./advent_of_code_2024/josh/day16/output.txt", "w")
    array_grid = [list(row) for row in grid]

    for node in nodes_on_path:
        array_grid[node[0]][node[1]] = "O"
    
    for row in array_grid:
        print("".join(row))
        output.write("".join(row) + "\n")

def render_path(grid: List[str], path: Path):
    array_grid = [list(row) for row in grid]

    for edge in path.edges:
        array_grid[edge[0][0]][edge[0][1]] = "O"
        array_grid[edge[1][0]][edge[1][1]] = "O"
    
    for row in array_grid:
        print("".join(row))

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

grid = input_file

edge_paths: Dict[Tuple[Tuple[int, int], Tuple[int, int]], List[Path]] = defaultdict(list)
seen_edges: Dict[Tuple[Tuple[int, int], Tuple[int, int]], int] = {}
start = Path(grid, [((len(grid) - 2, 0), (len(grid) - 2, 1))], 0)
frontier = [start]

heapify(frontier)

while frontier:
    next = heappop(frontier)
    # Update the list of paths that reach this end node
    next_last_edge = next.edges[-1]

    paths = next.extend()
    for path in paths:
        final_edge = path.edges[-1]
        if final_edge not in seen_edges:
            seen_edges[final_edge] = path.cost
            edge_paths[final_edge].append(path.copy())
            heappush(frontier, path)
        else:
            if edge_paths[final_edge][0].cost == path.cost:
                edge_paths[final_edge].append(path)

# We've now computed the cost to each node, including the end node. Identify anything on an 
# optimal path, which can come into the end node from one of 2 directions.
possible_end_edges = [
    ((1, len(grid[0]) - 3), (1, len(grid[0]) - 2)),
    ((2, len(grid[0]) - 2), (1, len(grid[0]) - 2))
]
min_total_cost = 99999999999999999999
min_paths = []
for edge in possible_end_edges:
    possible_end_paths = edge_paths[edge]
    for path in possible_end_paths:
        if path.cost < min_total_cost:
            min_total_cost = path.cost
            min_paths.append(path)

min_paths = list(filter(lambda path: path.cost == min_total_cost, min_paths))

nodes_on_path: Set[Tuple[int, int]] = set()
nodes_on_path.add((1, len(grid[0]) - 2))

for path in min_paths:
    nodes_on_path.update(add_path_nodes(path, len(path.edges) - 1))

nodes_on_path.remove((len(grid) - 2, 0))
    
print(f"Path length: {len(path.edges)}, cost: {path.cost}")
print(f"Nodes on paths: {len(nodes_on_path)}")
render(grid, nodes_on_path)