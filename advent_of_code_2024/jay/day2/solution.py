
def is_safe(array):
    is_increasing = True
    is_decreasing = True

    for i in range(len(array) - 1):
        if int(array[i]) >= int(array[i + 1]):
            is_increasing = False
        if int(array[i]) <= int(array[i + 1]):
            is_decreasing = False

    if is_increasing or is_decreasing:
        return all(abs(int(array[i]) - int(array[i + 1])) in {1, 2, 3} for i in range(len(array) - 1))
    else:
        return False

def is_difference_within_bounds_with_safety(array):
    for i in range(len(array)):
        tmpIndex = array.copy()
        tmpIndex.pop(i)
        if is_safe(tmpIndex):
            return True
        else:
            continue


reportData = {}

input = open('input.txt', 'r').read().splitlines()
for i in range(len(input)):
    reportData[i] = input[i].split()

unsafeReports = {}
unsafeReportCounter = 0

# Problem 1
safe = 0
for i in range(len(reportData)):
    if is_safe(reportData[i]):
        safe += 1
    else:
        unsafeReports[unsafeReportCounter] = reportData[i]
        unsafeReportCounter += 1

# Problem 2
maybeSafe = 0
for i in range(len(unsafeReports)):
    if is_difference_within_bounds_with_safety(unsafeReports[i]):
        maybeSafe += 1



print("Problem 1: " + str(safe))
maybeSafe += safe
print("Problem 2: " + str(maybeSafe))