def is_valid_pos(grid, x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])

def find_xmas(grid):
    word = "XMAS"
    word_length = len(word)
    word_count = 0

    directions = [
        (0, 1),  # Horizontal right
        (1, 0),  # Vertical down
        (0, -1),  # Horizontal left
        (-1, 0),  # Vertical up
        (1, 1),  # Diagonal down-right
        (-1, -1),  # Diagonal up-left
        (1, -1),  # Diagonal down-left
        (-1, 1),  # Diagonal up-right
    ]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            for dx, dy in directions:
                # Check for the word in the current direction
                found = True
                for k in range(word_length):
                    # i,j are current location in the grid i.e. current cursor location
                    # multiplying by the direction dx,dy results in moving the cursor in the direction of motion by k distance
                    nx, ny = i + k * dx, j + k * dy
                    # Check if the position is within the grid or the letter in the projected cursor position matches the element of the word.
                    if not is_valid_pos(grid, nx, ny) or grid[nx][ny] != word[k]:
                        found = False
                        break
                    # If we get through the loop, that means all characters in the direction match the word in that direction. Found stays True.
                if found:
                    word_count += 1
    return word_count

def find_x_mas(grid):
    word_count = 0
    # There are only 4 patterns for the X
    # M.M   M.S   S.S   S.M
    # .A.   .A.   .A.   .A.
    # S.S   M.S   M.M   S.M
    patterns = [
        {"top_left": "M", "top_right": "S", "center": "A", "bottom_left": "M", "bottom_right": "S"},
        {"top_left": "M", "top_right": "M", "center": "A", "bottom_left": "S", "bottom_right": "S"},
        {"top_left": "S", "top_right": "M", "center": "A", "bottom_left": "S", "bottom_right": "M"},
        {"top_left": "S", "top_right": "S", "center": "A", "bottom_left": "M", "bottom_right": "M"},
    ]

    # Check for the X-pattern centered at (i, j)
    # Because we're shooting for a pattern that is always only 1 element away from center, we
    # avoid the borders with this method by padding the borders by that 1 element.
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            # Extract diagonal characters
            top_left = grid[i - 1][j - 1]
            center = grid[i][j]
            bottom_right = grid[i + 1][j + 1]
            top_right = grid[i - 1][j + 1]
            bottom_left = grid[i + 1][j - 1]

            # Check against each pattern
            for pattern in patterns:
                if (
                    top_left == pattern["top_left"] and
                    top_right == pattern["top_right"] and
                    center == pattern["center"] and
                    bottom_left == pattern["bottom_left"] and
                    bottom_right == pattern["bottom_right"]
                ):
                    word_count += 1

    return word_count

input = open('input.txt', 'r').read()
# Build the Grid!
grid = [list(row) for row in input.splitlines()]

xmas_occurrences = find_xmas(grid)
x_mas_occurrences = find_x_mas(grid)

print("Solution 1: " + str(xmas_occurrences))
print("Solution 2: " + str(x_mas_occurrences))