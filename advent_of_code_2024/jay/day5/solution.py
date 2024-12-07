import re
from collections import defaultdict, deque

# Define the Structures
postrules = {}
prerules = {}
updates = []
correct_updates = []
incorrect_updates = []

# Build the adjacency list for the ordering rules
graph = defaultdict(list)
in_degree = defaultdict(int)

# GPT Function
def is_valid_order(update):
    """Check if the given update order is valid based on the rules."""
    local_in_degree = in_degree.copy()
    for page in update:
        if local_in_degree[page] != 0:
            return False
        for neighbor in graph[page]:
            local_in_degree[neighbor] -= 1
    return True


def reorder_update(update):
    """Reorder the update to follow the rules using topological sort."""
    local_graph = {p: [] for p in update}
    local_in_degree = {p: 0 for p in update}

    for p in update:
        for neighbor in graph[p]:
            if neighbor in update:
                local_graph[p].append(neighbor)
                local_in_degree[neighbor] += 1

    queue = deque([p for p in update if local_in_degree[p] == 0])
    sorted_update = []

    while queue:
        current = queue.popleft()
        sorted_update.append(current)
        for neighbor in local_graph[current]:
            local_in_degree[neighbor] -= 1
            if local_in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_update

# Jay Function
def is_correct_order(array):
    correct = True
    for k in range(len(array) - 1):
        if array[k+1] not in postrules[array[k]]:
            correct = False
        if k >= 1 and array[k-1] not in prerules[array[k]]:
            correct = False
    return correct

input = open('input.txt', 'r').read().splitlines()
for i in range(len(input)):
    if re.match(r"\d+\|\d+", input[i]):
        # We have a rule
        # GPT Code
        x, y = map(int, input[i].split('|'))
        graph[x].append(y)
        in_degree[y] += 1
        if x not in in_degree:
            in_degree[x] = 0

        # Jay Code
        key, value = map(int, input[i].split('|'))
        if key not in postrules:
            postrules[key] = []
        if key not in prerules:
            prerules[key] = []
        postrules[key].append(value)
        if value not in postrules:
            postrules[value] = []
        if value not in prerules:
            prerules[value] = []
        prerules[value].append(key)
    elif input[i] == "":
        continue
    elif re.match(r"\d+,\d+", input[i]):
        # We have an update
        update = []
        for item in input[i].split(','):
            update.append(int(item))
        updates.append(update)

for i in range(len(updates)):
    correct = is_correct_order(updates[i])
    if correct:
        correct_updates.append(updates[i])
    else:
        incorrect_updates.append(updates[i])

correct_middle_total = 0
for i in range(len(correct_updates)):
    middle_index = len(correct_updates[i]) // 2
    correct_middle_total += correct_updates[i][middle_index]

print("Solution 1: " + str(correct_middle_total))

# GPT Code
# Process updates
incorrect_updates_middle_sum = 0

# GPT couldn't find the Corrected vs. Uncorrected.
for update in incorrect_updates:
    if not is_valid_order(update):
        sorted_update = reorder_update(update)
        middle_index = len(sorted_update) // 2
        incorrect_updates_middle_sum += sorted_update[middle_index]

print("Solution 2: " + str(incorrect_updates_middle_sum))