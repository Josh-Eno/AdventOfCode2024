import re

# Constants
a_button_cost = 3
b_button_cost = 1

def win_the_game(game):
    win_moves = []
    cost = 0
    a1 = game['A'][0]
    a2 = game['A'][1]
    b1 = game['B'][0]
    b2 = game['B'][1]
    c1 = game['Prize'][0]
    c2 = game['Prize'][1]
    A = (b2 * c1 - b1 * c2) / (b2 * a1 - b1 * a2)
    B = (c1 - a1 * A) / b1
    if A == int(A) and B == int(B):
        win_moves.append((int(A), int(B)))

    for a, b in win_moves:
        cost += a * a_button_cost + b * b_button_cost
    return cost


def push_the_buttons(game, max_presses=100):
    min_cost = None
    # Loop through the button presses, most expensive button first. k
    for A_count in range(max_presses+1):
        for B_count in range(max_presses+1):
            # Check if we're there yet
            if (A_count * game['A'][0] + B_count * game['B'][0] == game['Prize'][0] and
                    A_count * game['A'][1] + B_count * game['B'][1] == game['Prize'][1]):
                # We have arrived at a solution. Calculate cost.
                cost = A_count * a_button_cost + B_count * b_button_cost
                # We might get here more than once. If this is the cheapest way, track it.
                if min_cost is None or cost < min_cost:
                    min_cost = cost
    return min_cost


games = []
# Parse the file to the data structures
# This is most definitely overkill.
with open('input.txt') as file:
    game = {}
    button_a_coords = ()
    button_b_coords = ()
    prize_coords = ()
    for line in file:
        line = line.strip()
        if line.startswith('Button A:'):
            button_a_coords = [int(x) for x in re.findall(r'X\+(\d+), Y\+(\d+)', line)[0]]
        elif line.startswith('Button B:'):
            button_b_coords = [int(x) for x in re.findall(r'X\+(\d+), Y\+(\d+)', line)[0]]
        elif line.startswith('Prize:'):
            prize_coords = [int(x) for x in re.findall(r'X=(\d+), Y=(\d+)', line)[0]]
            game['A'] = button_a_coords
            game['B'] = button_b_coords
            game['Prize'] = prize_coords
            games.append(game)

part_2_games = []
with open('input.txt') as file:
    game = {}
    button_a_coords = []
    button_b_coords = []
    prize_coords = []
    for line in file:
        line = line.strip()
        if line.startswith('Button A:'):
            button_a_coords = [int(x) for x in re.findall(r'X\+(\d+), Y\+(\d+)', line)[0]]
        elif line.startswith('Button B:'):
            button_b_coords = [int(x) for x in re.findall(r'X\+(\d+), Y\+(\d+)', line)[0]]
        elif line.startswith('Prize:'):
            prize_coords = [int(x) for x in re.findall(r'X=(\d+), Y=(\d+)', line)[0]]
            game['A'] = button_a_coords
            game['B'] = button_b_coords
            game['Prize'] = prize_coords
            game['Prize'][0] = prize_coords[0] + 10000000000000
            game['Prize'][1] = prize_coords[1] + 10000000000000
            part_2_games.append(game.copy())

solutions = []
part_2_solutions = []
for game in games:
    cost = push_the_buttons(game, max_presses=100)
    solutions.append(cost)

for game in part_2_games:
    cost = win_the_game(game)
    #print(f"Cost: {cost}")
    part_2_solutions.append(cost)

# Filter out games that are not solvable (cost = None)
solvable_costs = []
for solution in solutions:
    if solution is None:
        continue
    else:
        solvable_costs.append(solution)

# Filter out games that are not solvable (cost = None)
part_2_solvable_costs = []
for solution in part_2_solutions:
    if solution is None:
        continue
    else:
        part_2_solvable_costs.append(solution)

max_prizes = len(solvable_costs)
total_min_tokens = sum(solvable_costs)

part_2_max_prizes = len(part_2_solvable_costs)
part_2_total_min_tokens = sum(part_2_solvable_costs)

#print("Number of prizes solvable:", max_prizes)
print("Minimum total tokens to solve all solvable games (Part 1):", total_min_tokens)

#print("Number of prizes solvable (Part 2):", part_2_max_prizes)
print("Minimum total tokens to solve all solvable games (Part 2):", part_2_total_min_tokens)







