from typing import List

def is_safe(values: List[int]) -> bool:
    growing = values[0] < values[1]
    for idx, elem in enumerate(values):
        if idx == 0:
            continue
        diff = elem - values[idx - 1]
        if growing and (diff < 1 or diff > 3):
            return False
        if not growing and (diff > -1 or diff < -3):
            return False

    return True

def is_safe_dampened(values: List[int]) -> bool:
    safe = is_safe(values)
    idx_to_remove = 0
    while not safe and idx_to_remove < len(values):
        test_values = values.copy()
        test_values.pop(idx_to_remove)
        safe = is_safe(test_values)
        idx_to_remove += 1
    
    return safe

values = list(map(lambda x: list(
            map(int, x.split())
        ), 
        open("./advent_of_code/src/josh/day2/input.txt").read().splitlines()))

safe_vals = list(filter(is_safe, values))
damped_safe_vals = list(filter(is_safe_dampened, values))

print(f"Without dampener: {len(safe_vals)}")
print(f"With dampener: {len(damped_safe_vals)}")