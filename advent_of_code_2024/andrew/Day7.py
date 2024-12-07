import re
import math

def objOne(fileContent: str):
    lines = re.split("\n", fileContent)
    count = 0
    for line in lines:
        sumToObtain = int(re.split(":", line)[0])
        sequence = list(map(int, re.split(" ", re.split(":", line)[1])[1:]))
        count += sumToObtain if someSequenceOfOperatorsWorks(sequence, sumToObtain) else 0
    print(count)

def objTwo(fileContent:str):
    lines = re.split("\n", fileContent)
    count = 0
    lineNum = 0
    for line in lines:
        sumToObtain = int(re.split(":", line)[0])
        sequence = list(map(int, re.split(" ", re.split(":", line)[1])[1:]))
        print("Trying line " + str(lineNum) + "...")
        count += sumToObtain if someSequenceOfOperatorsWorks2(sequence, sumToObtain) else 0
        lineNum += 1
    print(count)

def someSequenceOfOperatorsWorks(seq: list, aim: int) -> bool:
    # Try every possible combination of operators
    for i in range(int(math.pow(2, len(seq) - 1))):
        # I.e. if list is 8 elements, i will go from 0 to 2^7-1, or 127, because there will be 127 combinations of operators: represented in binary
        binaryNum = str(f"{i:16b}") # This will give us 16 bits, more than enough. 
        operatorList = []
        for i in range(len(seq) - 1): # If there is 6 elements, there will be 5 operators and thus 5 binary numbers we need
            char = binaryNum[-1 - i] # Count backwards through the binary number
            if (char == "0" or char == "1"):
                operatorList.append((True if char == "1" else False))
        while len(operatorList) < len(seq)-1:
            operatorList.append(False)
        if evaluateSequenceWithOperators(seq, operatorList) == aim:
            return True
    return False

# By Poke on stack overflow
def ternary (n):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums))


def someSequenceOfOperatorsWorks2(seq: list, aim: int, debug=False) -> bool:
    # Try every possible combination of operators
    for i in range(int(math.pow(3, len(seq) - 1))):
        # I.e. if list is 4 elements, i will go from 0 to 3^4-1, or , because there will be 27 combinations of operators: represented in trinary
        trinaryNum = ternary(i) # This will give us 16 bits, more than enough. 
        #print("Trinary of " + str(i) + " is " + str(trinaryNum) + ". List was " + str(len(seq)) + " elements long")
        while len(trinaryNum) < len(seq)-1:
            trinaryNum = "0" + trinaryNum
        operatorList = []
        for i in range(len(seq) - 1): # If there is 6 elements, there will be 5 operators and thus 5 binary numbers we need
            char = trinaryNum[i]
            if (char == "0" or char == "1" or char == "2"):
                operatorList.append(int(char))
        while len(operatorList) < len(seq)-1:
            operatorList.append(False)
        if evaluateSequenceWithOperators(seq, operatorList, debug) == aim:
            return True
    return False


def evaluateSequenceWithOperators(sequence: list, operators: list, debug=False) -> int:
    # Operators should have a length 1 less than sequence
    # It should be a list of bools, True if mulitplying, False if adding
    sum = 0
    if debug:
        print(operators)
        if operators == [0, 1, 0]:
            print("Should work??")
    sum = sequence[0]
    for operator in range(len(operators)):
        if operators[operator] == 1:
            if debug:
                print("Multiplying, result will transform sum from " + str(sum) + " to " + str(sum * sequence[operator+1]))
            sum = sum * sequence[operator+1]
        elif operators[operator] == 0:
            if debug:
                print("Multiplying, result will transform sum from " + str(sum) + " to " + str(sum + sequence[operator+1]))
            sum += sequence[operator+1]
        elif operators[operator] == 2: # Third operator
            sum = int(str(sum) + str(sequence[operator+1]))
    # Account for multiplications without additions after
    return sum

if __name__ == "__main__":
    with open("advent_of_code_2024\\andrew\\Day7.txt", "r") as file:
        objTwo(file.read())