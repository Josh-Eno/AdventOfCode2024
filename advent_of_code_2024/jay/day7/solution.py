import re

def tests_good_here(target, numbers, operators):
    from itertools import product

    ops_count = len(numbers) - 1
    for ops in product(operators, repeat=ops_count):
        result = numbers[0]
        for i, op in enumerate(ops):
            if op == '+':
                result = result + numbers[i + 1]
            elif op == '*':
                result = result * numbers[i + 1]
            elif op == '||':
                result = int(str(result) + str(numbers[i + 1]))

        if result == target:
            return True

    return False

sum_of_results_1 = 0
sum_of_results_2 = 0
input = open('input.txt', 'r').read().splitlines()
for i in range(len(input)):
    matches = re.match(r"^(\d+)\:(.*)$", input[i])
    value_list = list(map(int, matches[2].split()))
    if tests_good_here(int(matches[1]), value_list, ['+', '*']):
        sum_of_results_1 += int(matches[1])
    if tests_good_here(int(matches[1]), value_list, ['+', '*', '||']):
        sum_of_results_2 += int(matches[1])

print("Solution 1: " + str(sum_of_results_1))
print("Solution 2: " + str(sum_of_results_2))

