def objOne(file):
    count = 0
    for line in file.readlines():
        array = []
        for element in line.split():
            array.append(int(element))
        if (isIncreasingSafely(array) or isDecreasingSafely(array)):
            count += 1
    print(count)

def objTwo(file):
    count = 0
    lineCount = 0
    for line in file.readlines():
        array = []
        for element in line.split():
            array.append(int(element))
        if (isIncreasingSafely(array, False) or isDecreasingSafely(array, False)):
            count += 1
        lineCount += 1
    print(count)

def isIncreasingSafely(array, takenOneOut=True):
    if takenOneOut:
        prev = array[0]
        for i in range(1, len(array), 1):
            if not ((array[i] > prev) and (array[i] <= prev + 3)):
                return False
            prev = array[i]
        return True
    else:
        for i in range(0, len(array), 1):
            copyArray = array.copy()
            copyArray.pop(i)
            if (isIncreasingSafely(copyArray)):
                return True

def isDecreasingSafely(array, takenOneOut=True):
    if takenOneOut:
        prev = array[0]
        for i in range(1, len(array), 1):
            if not ((array[i] < prev) and (array[i] >= prev - 3)):
                return False
            prev = array[i]
        return True
    else:
        for i in range(0, len(array), 1):
            copyArray = array.copy()
            copyArray.pop(i)
            if (isDecreasingSafely(copyArray)):
                return True

if __name__ == "__main__":
    with open("AndrewsSolutions\day2.txt", "r") as file:
        objTwo(file)