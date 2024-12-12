import re
import time
import doctest

global arrayOfTimes
arrayOfTimes = [0, 0, 0, 0] # How many times an opperation occured, how they all took
global splitDict
splitDict = {}
global multDict
multDict = {}

def objOne(fileContent: str):
    strToBlink = fileContent
    timeStep = time.process_time()
    for i in range(25):
        print("Blink number " + str(i))
        strToBlink = blink(strToBlink)
        print(timeStep)
        timeStep = time.process_time()
    
    print("There were " + str(len(re.split(" ", strToBlink))) + " stones!")

def objTwo(fileContent: str):
    arrToBlink = list(map(int, re.split(" ", fileContent)))
    # Convert it to a dictionary:
    dictToBlink = {}
    for stone in set(arrToBlink):
        dictToBlink[stone] = arrToBlink.count(stone)
    print(dictToBlink)

    timeStep = time.process_time()
    for i in range(75):
        print("Blink number " + str(i))
        dictToBlink = blinkEfficientest(dictToBlink)
        print(timeStep)
        timeStep = time.process_time()
    
    #print(dictToBlink)
    count = 0

    #print("{", end="")
    for key in dictToBlink.keys():
        #print(str(key) + ": " + str(dictToBlink[key]), end=", ")
        count += dictToBlink[key]
        #print("Adding " + str(dictToBlink[key]))
    #print()
    
    print("There were " + str(count) + " stones!")

def blink(stonesLine: str):
    stonesArray = re.split(" ", stonesLine)
    stonesToInsert = []
    for stoneIndex in range(len(stonesArray)):
        # Follow the rules:
        if int(stonesArray[stoneIndex]) == 0:
            stonesArray[stoneIndex] = "1"
        elif len(stonesArray[stoneIndex]) % 2 == 0:
            stone = stonesArray[stoneIndex]
            stonesToInsert.append([stone[int(len(stone)/2):], stoneIndex+1])
            stonesArray[stoneIndex] = str(int(stone[:int(len(stone)/2)]))
        else:
            stonesArray[stoneIndex] = str(int(stonesArray[stoneIndex]) * 2024)
    
    while len(stonesToInsert) != 0:
        stonesArray.insert(stonesToInsert[0][1], str(int(stonesToInsert[0][0])))
        stonesToInsert.pop(0)
        for i in range(0, len(stonesToInsert), 1):
            stonesToInsert[i][1] += 1
    
    return stonesToString(stonesArray)

def stonesToString(stones: list):
    returnString = ""
    for stone in stones:
        returnString += str(stone) + " "
    #print("Got " + str(stones) + ", returning " + returnString[:-1])
    return returnString[:-1]

def blinkEfficient(stones: list):
    '''
    >>> blinkEfficient([253,0,2024,14168])
    [512072, 1, 20, 24, 28676032]
    '''
    global arrayOfTimes
    global splitDict
    if len(stones) > 1 and len(stones) % 2 == 0: # Split into two threads (this could be very bad lol)
        return blinkEfficient(stones[:int(len(stones)/2)]) + blinkEfficient(stones[int(len(stones)/2):])
    elif len(stones) > 1:
        return blinkEfficient(stones[:int((len(stones)-1)/2)]) + blinkEfficient(stones[int((len(stones)-1)/2):])
    else:
        if stones[0] == 0:
            return [1]
        elif len(str(stones[0]))%2 == 0:
            base = time.process_time()
            if stones[0] in splitDict.keys():
                returnVal = splitDict[stones[0]]
            else:
                returnVal = [int(str(stones[0])[:int(len(str(stones[0]))/2)]), int(str(stones[0])[int(len(str(stones[0]))/2):])]
                splitDict[stones[0]] = returnVal # Hopefuly this doesn't get deleted
            arrayOfTimes[1] += 1
            arrayOfTimes[0] += time.process_time() - base
            return returnVal
        else:
            base = time.process_time()
            if stones[0] in multDict.keys():
                returnVal = [multDict[stones[0]]]
            else:
                returnVal = [2024 * stones[0]]
                multDict[stones[0]] = int(stones[0]) * 2024
            arrayOfTimes[3] += 1
            arrayOfTimes[2] += time.process_time() - base
            return returnVal

def blinkEvenEfficienter(stones: list):
    '''
    >>> blinkEfficient([253,0,2024,14168])
    [512072, 1, 20, 24, 28676032]
    '''
    returnArray = []
    for stone in set(stones):
        count = stones.count(stone)
        stonesToAppend = []
        if stone == 0:
            stonesToAppend = [1]
        elif len(str(stone)) % 2 == 0:
            stonesToAppend = [int(str(stone)[:int(len(str(stone))/2)]), int(str(stone)[int(len(str(stone))/2):])]
        else:
            stonesToAppend = [stone * 2024]
        for st in stonesToAppend:
            for i in range(count):
                returnArray.append(st)
    
    return returnArray

def blinkEfficientest(stones: dict):
    '''
    >>> blinkEfficientest({253:1,0:1,2024:1,14168:1})
    {512072: 1, 1: 1, 20: 1, 24: 1, 28676032: 1}
    >>> blinkEfficientest({2024: 78})
    {20: 78, 24: 78}
    >>> blinkEfficientest({512:1, 72:1, 2024:1, 2:2, 0:1, 4:1, 2867:1, 6032:1})
    {1036288: 1, 7: 1, 2: 1, 20: 1, 24: 1, 4048: 2, 1: 1, 8096: 1, 28: 1, 67: 1, 60: 1, 32: 1}
    >>> blinkEfficientest({0: 100})
    {1: 100}
    '''
    returnDict = {}
    for key in stones.keys():
        if key == 0:
            if 1 in returnDict.keys():
                returnDict[1] = returnDict[1] + stones[0]
            else:
                returnDict[1] = stones[0]
        elif len(str(key)) % 2 == 0:
            if int(str(key)[:int(len(str(key))/2)]) in returnDict.keys():
                returnDict[int(str(key)[:int(len(str(key))/2)])] = returnDict[int(str(key)[:int(len(str(key))/2)])] + stones[key]
            else:
                returnDict[int(str(key)[:int(len(str(key))/2)])] = stones[key]
            if int(str(key)[int(len(str(key))/2):]) in returnDict.keys():
                returnDict[int(str(key)[int(len(str(key))/2):])] = returnDict[int(str(key)[int(len(str(key))/2):])] + stones[key]
            else:
                returnDict[int(str(key)[int(len(str(key))/2):])] = stones[key]
        else:
            if key * 2024 in returnDict.keys():
                returnDict[key * 2024] = returnDict[key * 2024] + stones[key]
            else:
                returnDict[key * 2024] = stones[key]
    return returnDict

if __name__ == "__main__":
    doctest.testmod()
    with open("advent_of_code_2024\\andrew\\Day11.txt", "r") as file:
        objTwo(file.read())