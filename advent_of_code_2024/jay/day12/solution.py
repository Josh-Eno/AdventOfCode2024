from collections import deque

from Tools.scripts.var_access_benchmark import loop_overhead


def in_bounds(grid, pos):
    max_rows = len(grid)
    max_cols = len(grid[0]) if max_rows > 0 else 0
    return 0 <= pos[0] < max_rows and 0 <= pos[1] < max_cols

# Find the neighbors. GPT had a more complicated one, but this one is easier to understand.
def neighbors(r, c, rows, cols):
    if r > 0:
        yield r - 1, c
    if r < rows - 1:
        yield r + 1, c
    if c > 0:
        yield r, c - 1
    if c < cols - 1:
        yield r, c + 1

# Handy video, that. https://youtu.be/xlVX7dXLS64
def find_garden_plot(grid, start_r, start_c, visited):
    rows, cols = len(grid), len(grid[0])
    # Grab the value of the garden type to start with
    plot_type = grid[start_r][start_c]
    queue = deque([(start_r, start_c)])
    # Don't forget to visit the starting coords...
    visited[start_r][start_c] = True

    area = 0
    perimeter = 0
    corners = 0

    # Helper Function
    def local_in_bounds(r, c):
        max_rows = len(grid)
        max_cols = len(grid[0]) if max_rows > 0 else 0
        return 0 <= r < max_rows and 0 <= c < max_cols

    while queue:
        r, c = queue.popleft()
        # Since we're only following neighbors, everything we process in the queue be part of the area.
        area += 1
        loop_corners = 0

        # Debugging Function.
        def print_grid(r, c):
            surrounding = [
                (r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
                (r, c - 1), (r, c), (r, c + 1),
                (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)
            ]
            rowcounter = 1
            print("Grid for (" + str(r) + ", " + str(c) + ")")
            for neighbor in surrounding:
                if not local_in_bounds(neighbor[0], neighbor[1]):
                    print('.', end='')
                elif neighbor[0] == 0 and neighbor[1] == 0:
                    print(plot_type, end='')
                else:
                    print(str(grid[neighbor[0]][neighbor[1]]), end='')
                if rowcounter == 3:
                    print("")
                    rowcounter = 1
                else:
                    rowcounter += 1

        def get_val(r,c):
            if not local_in_bounds(r, c):
                return '.'
            else:
                return str(grid[r][c])


        """
        Logic Helper
        1 2 3
        4 5 6
        7 8 9
        
        (r-1,c-1) (r-1,c) (r-1,c+1)
         (r,c-1)   (r,c)   (r,c+1)
        (r+1,c-1) (r+1,c) (r+1,c+1)
        """

        # This is an outside corner if:
        # 4 and 2 are different
        if get_val(r,c-1) != plot_type and get_val(r-1,c) != plot_type:
            loop_corners += 1
        # 2 and 6 are different
        if get_val(r-1,c) != plot_type and get_val(r,c+1) != plot_type:
            loop_corners += 1
        # 6 and 8 are different
        if get_val(r,c+1) != plot_type and get_val(r+1,c) != plot_type:
            loop_corners += 1
        # 8 and 4 are different
        if get_val(r+1,c) != plot_type and get_val(r,c-1) != plot_type:
            loop_corners += 1
        # This is an inside corner if:
        # 4 and 2 are the same, and 1 is different
        if get_val(r,c-1) == plot_type and get_val(r-1,c) == plot_type and get_val(r-1,c-1) != plot_type:
            loop_corners += 1
        # 2 and 6 are the same, and 3 is different
        if get_val(r-1,c) == plot_type and get_val(r,c+1) == plot_type and get_val(r-1,c+1) != plot_type:
            loop_corners += 1
        # 6 and 8 are the same, and 9 is different
        if get_val(r,c+1) == plot_type and get_val(r+1,c) == plot_type and get_val(r+1,c+1) != plot_type:
            loop_corners += 1
        # 8 and 4 are the same, and 7 is different
        if get_val(r+1,c) == plot_type and get_val(r,c-1) == plot_type and get_val(r+1,c-1) != plot_type:
            loop_corners += 1

        # Find all the neighbors of this plot, and track the fencing.
        # Count the neighbors so we know how many fences to count for this plot.
        plot_neighbors = 0
        for nr, nc in neighbors(r, c, rows, cols):
            if grid[nr][nc] == plot_type:
                plot_neighbors += 1
                if not visited[nr][nc]:
                    visited[nr][nc] = True
                    queue.append((nr, nc))
        # Assume 4 sides, less the sides that have neighbors that match the plot type.
        perimeter += (4 - plot_neighbors)
        #if loop_corners > 0:
        #    print("Corners: " + str(loop_corners))
        #    print(print_grid(r,c))
        corners += loop_corners


    return area, perimeter, corners

with open('input.txt') as file:
    grid = [line.strip() for line in file]

# Setup the Visited map
rows, cols = len(grid), len(grid[0])
visited = []
for i in range(rows):
    row = []
    for j in range(cols):
        row.append(False)
    visited.append(row)

total_price = 0
discount_price = 0

for r in range(rows):
    for c in range(cols):
        if not visited[r][c]:
            area, perimeter, corners = find_garden_plot(grid, r, c, visited)
            price = area * perimeter
            side_price = area * corners
            total_price += price
            discount_price += side_price


print("Solution 1: " + str(total_price))
print("Solution 2: " + str(discount_price))
