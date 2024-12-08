
# Build the Grid
original_grid = []
with open('input.txt') as file:
    for line in file:
        original_grid.append(list(line.strip()))

# Define some things...
rows = len(original_grid)
cols = len(original_grid[0])
#guard_pos_x, guard_pos_y = 0, 0
visited = []
vectormap = {}
block_options = []
directions = {
    'N': (-1, 0),  # Move up
    'S': (1, 0),   # Move down
    'E': (0, 1),   # Move right
    'W': (0, -1),  # Move left
}
direction_rotation = {
    'N': 'E',
    'E': 'S',
    'S': 'W',
    'W': 'N'
}
# We always start facing North...
current_direction = 'N'

def find_guard():
    global guard_pos_x, guard_pos_y, visited, original_grid
    for y, row in enumerate(original_grid):
        if '^' in row:
            guard_pos_x = row.index('^')
            guard_pos_y = y
            visited.append([y, guard_pos_x])
            vectormap[(y, guard_pos_x)] = current_direction
            return [guard_pos_x, guard_pos_x]

guard_pos_x, guard_pos_y = find_guard()

def on_grid(grid, pos):
    if 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0]):
        return True

def is_loop(grid, start_pos, direction):
    cur_direction = direction
    num_moves = 0
    cur_pos = start_pos
    grid_size = len(grid) * len(grid[0])
    next_pos = [start_pos[0] + directions[cur_direction][0],
                start_pos[1] + directions[cur_direction][1]]
    while on_grid(grid, cur_pos) and num_moves < grid_size:
        if grid[next_pos[0]][next_pos[1]] == '#':
            cur_direction = direction_rotation[cur_direction]
            continue
        cur_pos = [next_pos[0]][next_pos[1]]
        num_moves += 1
    print("Gave Up")
    return on_grid(grid, cur_pos)

def is_in_visited(coords):
    for i in visited:
        if i[0] == coords[0] and i[1] == coords[1]:
            return True
    return False

loop = 0
while True:
    guard_pos_x_next = guard_pos_x + directions[current_direction][1]
    guard_pos_y_next = guard_pos_y + directions[current_direction][0]
    #if 0 <= guard_pos_y_next < rows and 0 <= guard_pos_x_next < cols:
    if on_grid(original_grid, [guard_pos_y_next, guard_pos_x_next]):
        # If we hit an object, switch directions
        if original_grid[guard_pos_y_next][guard_pos_x_next] == '#':
            current_direction = direction_rotation[current_direction]
            continue
        if not is_in_visited([guard_pos_y_next,guard_pos_x_next]):
            visited.append([guard_pos_y_next,guard_pos_x_next])
            vectormap[(guard_pos_y_next,guard_pos_x_next)] = current_direction
        else:
            print("Next position (" + str(guard_pos_y_next) + ", " + str(guard_pos_x_next) + ") has been visited." )
            if vectormap[(guard_pos_y_next,guard_pos_x_next)] == direction_rotation[current_direction]:
                print("We're currently headed " + current_direction + ". The next location's vector last time was " + str(
                    vectormap[(guard_pos_y_next,guard_pos_x_next)]) + ". Turning should put us into a loop.")
                future_guard_pos_y_next = guard_pos_y_next + directions[current_direction][0]
                future_guard_pos_x_next = guard_pos_x_next + directions[current_direction][1]
                if [future_guard_pos_y_next, future_guard_pos_x_next] in block_options:
                    print("Shit. We've been her before.")
                block_options.append([future_guard_pos_y_next, future_guard_pos_x_next])
                print("Placing a Block at (" + str(future_guard_pos_y_next) + ", " + str(future_guard_pos_x_next) + ") would trigger a turn on to the previous path.")
                loop += 1
            else:
                print(
                    "We're currently headed " + current_direction + ". The next location's vector last time was " + str(
                        vectormap[(guard_pos_y_next, guard_pos_x_next)]) + ". (Not a right turn!)")
        guard_pos_y += directions[current_direction][0]
        guard_pos_x += directions[current_direction][1]
        loop += 1
    else:
        break

print("Solution 1: " + str(len(visited)))
print("Solution 2: " + str(len(block_options)))
