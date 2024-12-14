import re

def robot_dance(robots, grid_width, grid_height, time):
    for i, (x, y, vx, vy) in enumerate(robots):
        # We don't need to iterate here, just multiplying by time gets the result.
        # Do X and Y individually. Mod based on height/width does the "looping".
        new_x = (x + vx * time) % grid_width
        new_y = (y + vy * time) % grid_height
        robots[i] = (new_x, new_y, vx, vy)
    return robots

def build_robot_grid(robots, columns, rows):
    grid = []
    for _ in range(rows):
        grid.append(['.'] * columns)

    # Populate the grid with the robots
    for i, (x, y, vx, vy) in enumerate(robots):
        grid[y][x] = '*'

    return grid

def print_grid(grid):
    for row in grid:
        print("".join(row))

def count_quadrants(robots, grid_width, grid_height):
    tl = 0
    tr = 0
    bl = 0
    br = 0
    for (x, y, vx, vy) in robots:
        # Top Left
        if x < grid_width // 2 and y < grid_height // 2:
            tl += 1
        # Top Right
        elif x > grid_width // 2 and y < grid_height // 2:
            tr += 1
        # Bottom Left
        elif x < grid_width // 2 and y > grid_height // 2:
            bl += 1
        # Bottom Right
        elif x > grid_width // 2 and y > grid_height // 2:
            br += 1

    return tl, tr, bl, br

robots = []
input = open('input.txt', 'r').read().splitlines()
for i in range(len(input)):
    match = re.match(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', input[i])
    # Make them ints because...math
    robot_data = list(map(int, match.groups()))
    robots.append((robot_data[0], robot_data[1], robot_data[2], robot_data[3]))

# Test Grid 11x7. Actual Input Grid 101x103
grid_width = 101
grid_height = 103
time = 100

moved_robots = robot_dance(robots.copy(), grid_width, grid_height, time)
tl, tr, bl, br = count_quadrants(moved_robots, grid_width, grid_height)
safety_factor = tl * tr * bl * br

print(f"Solution 1: {safety_factor}")

def has_tree(grid):
    for row in grid:
        # 8 seems to be the minimum in order to capture the sync of the tree.
        regexp = re.compile(r'\*{10}')
        if regexp.search("".join(row)):
            return True
    return False

loop = 100
while True:
    moved_robots = robot_dance(robots.copy(), grid_width, grid_height, loop)
    if has_tree(build_robot_grid(moved_robots, grid_width, grid_height)):
        print_grid(build_robot_grid(moved_robots, grid_width, grid_height))
        print(f"Found solution 2 at loop {loop}.")
        break
    if loop >= 10000000:
        print(f"After {loop} loops, guessing there probably isn't going to be a tree....")
        break
    loop += 1


