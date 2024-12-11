from collections import deque

def neighbors(r, c, rows, cols):
    # Return valid up/down/left/right neighbors
    for nr, nc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

def find_trailhead_scores(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Identify all trailheads (cells of height 0)
    trailheads = [(r,c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]

    total_score = 0

    # For each trailhead, we find all distinct reachable '9' cells
    # A BFS/DFS approach:
    for start_r, start_c in trailheads:
        # We'll keep track of visited cells to avoid re-processing
        visited = [[False]*cols for _ in range(rows)]
        visited[start_r][start_c] = True

        # Queue for BFS: (row, col)
        queue = deque([(start_r, start_c)])
        reachable_nines = set()

        while queue:
            r, c = queue.popleft()
            current_height = grid[r][c]

            # If we reach a cell of height 9, record it
            if current_height == 9:
                reachable_nines.add((r,c))
                # Once at height 9, we don't continue further upward (no higher than 9)
                continue

            # Otherwise, try to move to next height = current_height + 1
            next_height = current_height + 1
            for nr, nc in neighbors(r,c,rows,cols):
                if not visited[nr][nc] and grid[nr][nc] == next_height:
                    visited[nr][nc] = True
                    queue.append((nr, nc))

        # The score for this trailhead is the number of reachable unique 9-cells
        total_score += len(reachable_nines)

    return total_score

def find_trailhead_ratings(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # DP array for memoization: number of distinct paths from (r,c) to a '9'
    dp = [[None] * cols for _ in range(rows)]

    def get_paths(r, c):
        if dp[r][c] is not None:
            return dp[r][c]

        current_height = grid[r][c]
        if current_height == 9:
            dp[r][c] = 1
            return 1

        count = 0
        next_height = current_height + 1
        for nr, nc in neighbors(r, c, rows, cols):
            if grid[nr][nc] == next_height:
                count += get_paths(nr, nc)

        dp[r][c] = count
        return count

    # Compute dp for all cells
    for r in range(rows):
        for c in range(cols):
            if dp[r][c] is None:
                get_paths(r, c)

    # Identify all trailheads (cells of height 0) and sum their dp values
    total_rating = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                total_rating += dp[r][c]

    return total_rating

with open('input.txt') as file:
    grid = [list(map(int, list(line.strip()))) for line in file]

total_score = find_trailhead_scores(grid)
total_rating = find_trailhead_ratings(grid)
print("Solution 1: " + str(total_score))
print("Solution 2: " + str(total_rating))
