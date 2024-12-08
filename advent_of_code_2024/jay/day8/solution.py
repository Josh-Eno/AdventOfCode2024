from math import gcd

def in_bounds(grid, pos):
    max_rows = len(grid)
    max_cols = len(grid[0]) if max_rows > 0 else 0
    return 0 <= pos[0] < max_rows and 0 <= pos[1] < max_cols

def find_antinodes(grid, resonance):
    # Capture all the Antennas in a map by frequency.
    antennas = {}
    for r in range(len(grid)):
        for c in range(len(grid[0]) if len(grid) > 0 else 0):
            ch = grid[r][c]
            if ch != '.':
                antennas.setdefault(ch, []).append((r, c))

    antinodes = set()
    # For each frequency, consider all pairs of antennas
    for freq, positions in antennas.items():
        n = len(positions)
        if n < 2:
            print("Less than 2 antennas, no antinodes for frequency {}".format(freq))
            continue

        #Loop through for unique antenna pairs
        for i in range(n):
            for j in range(i + 1, n):
                # Antenna Positions
                a1_r, a1_c = positions[i]
                a2_r, a2_c = positions[j]

                # Compute the antinodes:
                if resonance:
                    # Find the slope/steps
                    dr = a2_r - a1_r
                    dc = a2_c - a1_c
                    g = gcd(dr, dc)
                    dr_step = dr // g
                    dc_step = dc // g

                    # Move one direction, log all the resonance points.
                    # Doesn't matter what tower we start with
                    rr, cc = a1_r, a1_c
                    while in_bounds(grid, (rr, cc)):
                        antinodes.add((rr, cc))
                        rr += dr_step
                        cc += dc_step

                    # Move the other direction
                    # We already collected the original tower, so step first.
                    rr, cc = a1_r - dr_step, a1_c - dc_step
                    while in_bounds(grid, (rr, cc)):
                        antinodes.add((rr, cc))
                        rr -= dr_step
                        cc -= dc_step

                else:
                    # A = (2P - Q)
                    r_a = 2 * a1_r - a2_r
                    c_a = 2 * a1_c - a2_c
                    # B = (2Q - P)
                    r_b = 2 * a2_r - a1_r
                    c_b = 2 * a2_c - a1_c

                    # Check bounds and add if valid
                    if in_bounds(grid, (r_a, c_a)):
                        antinodes.add((r_a, c_a))
                    if in_bounds(grid, (r_b, c_b)):
                        antinodes.add((r_b, c_b))

    return len(antinodes)

input = open('input.txt', 'r').read().splitlines()
antinodes_solution_1 = find_antinodes(input, False)
antinodes_solution_2 = find_antinodes(input, True)
print("Solution 1: " + str(antinodes_solution_1))
print("Solution 2: " + str(antinodes_solution_2))

