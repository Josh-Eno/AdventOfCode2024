from typing import Set, Tuple

input_file = open("./advent_of_code_2024/josh/day18/input.txt").read().splitlines()
grid_file = [["."] * 71 for _ in range(71)]
dest_file = (70, 70)

input_test = [
    "5,4",
    "4,2",
    "4,5",
    "3,0",
    "2,1",
    "6,3",
    "2,4",
    "1,5",
    "0,6",
    "3,3",
    "2,6",
    "5,1",
    "1,2",
    "5,5",
    "2,5",
    "6,5",
    "1,4",
    "0,4",
    "6,4",
    "1,1",
    "6,1",
    "1,0",
    "0,5",
    "1,6",
    "2,0",
]
grid_test = [["."] * 7 for _ in range(7)]
dest_test = (6, 6)

input = input_file
coords = list(map(lambda x: tuple(map(lambda x: int(x), x.split(","))), input))
grid = grid_file
dest = dest_file

start = (0, 0)
frontier: Set[Tuple[int, int]] = {start}
test_coords = []
test_grid = [row[:] for row in grid]

succeeded = True
for last_idx in range(len(coords)):
    if not succeeded:
        break
    steps = 0
    seen: Set[Tuple[int, int]] = set()
    frontier: Set[Tuple[int, int]] = {start}
    test_coords = coords[:last_idx]
    test_grid = [row[:] for row in grid]
    for c in test_coords:
        test_grid[c[1]][c[0]] = "#"

    while frontier and dest not in frontier:
        new_frontier = set()
        for coord in frontier:
            x, y = coord
            seen.add((x, y))
            test_grid[y][x] = "0"
            if x > 0 and test_grid[y][x - 1] != "#" and (x - 1, y) not in seen:
                new_frontier.add((x - 1, y))
            if x < len(test_grid[0]) - 1 and test_grid[y][x + 1] != "#" and (x + 1, y) not in seen:
                new_frontier.add((x + 1, y))
            if y > 0 and test_grid[y - 1][x] != "#" and (x, y - 1) not in seen:
                new_frontier.add((x, y - 1))
            if y < len(test_grid) - 1 and test_grid[y + 1][x] != "#" and (x, y + 1) not in seen:
                new_frontier.add((x, y + 1))

        frontier = new_frontier
        steps += 1

    if dest not in frontier:
        succeeded = False
        print(f"Failed at {test_coords[-1]}")
        print("\n".join(["".join(row) for row in test_grid]))
        break
