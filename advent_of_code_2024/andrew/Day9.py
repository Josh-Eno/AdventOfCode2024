def objOne(fileContent: str):
    # We are going with an array representation, we'll see if thats a good idea later
    line = fileContent;
    fileArray = []
    for i in range(0, len(line), 2):
        for j in range(int(line[i])):
                fileArray.append(int(i/2))
        if (len(line) > i+1):
             for k in range(int(line[i+1])):
                  fileArray.append(-1)
    #print(fileArray)

    defrag(fileArray)

    #print(fileArray)

    # Compute checksum
    checksum = 0
    for elementIndex in range(len(fileArray)):
        checksum += (elementIndex * fileArray[elementIndex] if fileArray[elementIndex] != -1 else 0)
    print(checksum)

def objTwo(fileContent: str):
    # We are going with an array representation, we'll see if thats a good idea later
    line = fileContent.strip();
    fileArray = []
    for i in range(0, len(line), 2):
        for j in range(int(line[i])):
                fileArray.append(int(i/2))
        if (len(line) > i+1):
             for k in range(int(line[i+1])):
                  fileArray.append(-1)
    #print(fileArray)
    
    '''
    for element in fileArray:
        if element != -1:
            print(element, end="")
        else:
            print(".", end="")
    print()'''

    defragTwo(fileArray)

    '''
    for element in fileArray:
        if element != -1:
            print(element, end="")
        else:
            print(".", end="")
    print()'''

    # Compute checksum
    checksum = 0
    for elementIndex in range(len(fileArray)):
        checksum += (elementIndex * fileArray[elementIndex] if fileArray[elementIndex] != -1 else 0)
    print(checksum)

def defrag(fileArr: list):
    unsorted = True
    while unsorted:
        
        # Find the rightmost number and swap it with the leftmost -1
        leftmostEmptyIndex = fileArr.index(-1)
        rightmostNumberIndex = -1
        for i in range(len(fileArr)-1, 0, -1):
            if fileArr[i] != -1:
                rightmostNumberIndex = i
                break
        
        # Swap them
        temp = fileArr[leftmostEmptyIndex]
        fileArr[leftmostEmptyIndex] = fileArr[rightmostNumberIndex]
        fileArr[rightmostNumberIndex] = temp

        print("Swapped " + str(leftmostEmptyIndex) + " and " + str(rightmostNumberIndex))

        # Verify sorted or not
        countingElements = True
        unsorted = False
        for element in fileArr:
            #print(element, end="")
            if element == -1:
                countingElements = False
            elif (not countingElements) and (element != -1):
                unsorted = True
        #print()

def defragTwo(fileArr: list):
    maxElement = -1
    for i in range(len(fileArr) - 1, 0, -1):
        if fileArr[i] != -1:
            maxElement = fileArr[i]
            break
    movedIds = []

    whitespaceSections = []

    countingWhitespace = False
    for i in range(len(fileArr)):
        if fileArr[i] == -1 and countingWhitespace == False:
            whitespaceSections.append([i])
            countingWhitespace = True
        elif fileArr[i] != -1 and countingWhitespace:
            whitespaceSections[len(whitespaceSections)-1] = [whitespaceSections[len(whitespaceSections)-1][0], i - whitespaceSections[len(whitespaceSections)-1][0]] # [start, length]
            countingWhitespace = False

    for fileNum in range(maxElement, 0, -1):
        # Find the rightmost file and its size
        rightmostId = fileNum

        rightmostFileStart = fileArr.index(rightmostId)
        rightmostFileEnd = rightmostFileStart + fileArr.count(rightmostId) # The index of the last letter + 1

        #print("Rightmost id was " + str(rightmostId) + " and its start was " + str(rightmostFileStart) + " and its size was " + str(rightmostFileEnd - rightmostFileStart))
        
        whitespaceNeeded = rightmostFileEnd - rightmostFileStart
        #print("Whitespace needed is " + str(whitespaceNeeded))


        # Find the leftmost whitespace that fits
        # We have to search through whitespaceSections to find a section that'll fit
        whitespaceStart = -1
        whitespaceEnd = -1

        for i in range(len(whitespaceSections)):
            if whitespaceSections[i][1] >= whitespaceNeeded and whitespaceSections[i][0] < rightmostFileStart:
                whitespaceStart = whitespaceSections[i][0]
                whitespaceEnd = whitespaceStart + whitespaceSections[i][1]
                if whitespaceSections[i][1] >= whitespaceNeeded:
                    arrayToAppend = [whitespaceEnd - (whitespaceSections[i][1] - whitespaceNeeded), (whitespaceSections[i][1] - whitespaceNeeded)]
                    whitespaceSections.pop(i)
                    whitespaceSections.insert(i, arrayToAppend)
                else:
                    whitespaceSections.pop(i)
                break

        if whitespaceStart != -1 and not (fileNum in movedIds): # Or whitespaceStart != -1
            #print("Swapped file starting at " + str(rightmostFileStart) + " and whitespace starting at " + str(whitespaceStart) + " and ending at " + str(whitespaceEnd))
            # Swap them
            movedIds.append(fileNum)
            for i in range(whitespaceNeeded):
                temp = fileArr[whitespaceStart + i]
                fileArr[whitespaceStart + i] = fileArr[rightmostFileStart + i]
                fileArr[rightmostFileStart + i] = temp

        # Verify sorted or not
        countingElements = True
        unsorted = False
        for element in fileArr:
            #if element != -1:
            #    print(element, end="")
            #else:
            #    print(".", end="")
            if element == -1:
                countingElements = False
            elif (not countingElements) and (element != -1):
                unsorted = True
        #print()
        movedIds.append(fileNum)

if __name__ == '__main__':
    with open("advent_of_code_2024\\andrew\\Day9.txt", "r") as file:
        objTwo(file.read())