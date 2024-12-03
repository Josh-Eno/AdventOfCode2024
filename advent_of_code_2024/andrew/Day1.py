# Day 1

def first(textFile):
    # Parse each line of the text file: put the left number in one sorted array, and right number in another
    left = []
    right = []
    for line in file.readlines():
        split = line.split()
        left.append(int(split[0]))
        right.append(int(split[1]))
    left.sort()
    right.sort()
    differences = []
    total = 0
    for i in range(len(left)):
        differences.append(abs(left[i] - right[i]))
        total += abs(left[i] - right[i])
    print(total)

def second(textFile):
    left = []
    right = []
    for line in file.readlines():
        split = line.split()
        left.append(int(split[0]))
        right.append(int(split[1]))
    total = 0
    for i in range(len(left)):
        total += left[i] * right.count(left[i])
    print(total)

if __name__ == "__main__":
    with open("day1.txt", "r") as file: 
        print("First answer:")
        first(file)
    with open("day1.txt", "r") as file:
        print("Second answer:")
        second(file)