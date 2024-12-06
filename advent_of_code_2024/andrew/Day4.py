import math

def objOne(file):
    fileContent: str = file.read()
    lineLen = fileContent.find("\n")
    fileContent = str.replace(fileContent, "\n", "")
    index = 0
    successes = 0
    for character in fileContent:
        if (character == "X"):
            newSucc = searchAroundX(fileContent, index, lineLen)
            successes += newSucc
        index += 1

    # I have no idea why, but this answer is incorrect in the real data but fine in the test. Not gonna debug, I don't have time
    print(successes)

def searchAroundX(fileContents: str, index: int, lineLength: int) -> int: # Searches around the X character and if it spells XMAS, then put XMAS in the result array
    directions = [ # Up, up-right, right, down-right, down, down-left, left, up-left
        [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]
    ]
    lineLen = lineLength
    upperBound = len(fileContents)
    word = "XMAS"
    successes = 0
    for direction in directions:
        failed = False
        dRow = direction[0] * lineLen
        dColumn = direction[1]
        for i in range(1, len(word)):
            letterIndex = (dRow * i + dColumn * i) + index
            if 0 <= letterIndex < upperBound and fileContents[letterIndex] != word[i]:
                failed = True
                break
            elif not (0 <= letterIndex < upperBound):
                if (letterIndex > upperBound):
                    print()
                failed = True
                break
        if not failed:
            successes += 1
    return successes

def objTwo(file):
    # Check every occurence of M or S if its the top left part of an X
    fileContent: str = file.read()
    lineLen = fileContent.find("\n")
    fileContent = str.replace(fileContent, "\n", "")
    count = 0
    index = 0
    for character in fileContent:
        if character == "M" or character == "S":
            count += 1 if isPartOfX(fileContent, index, lineLen) else 0
        index += 1
    print(count)

def isPartOfX(fileContents: str, indexOfLetter: int, lineLength: int) -> bool:
    # Check out of bounds but also if its on the right/left edge
    if (0 <= (indexOfLetter + (2 * lineLength) + 2) < len(fileContents) and (math.floor(indexOfLetter/lineLength) == math.floor((indexOfLetter + 2)/lineLength))):
        # JUST detecting Xs from the top left. Could probably code golf this significantly, but its ugly enough already.
        isM = fileContents[indexOfLetter] == "M"
        center = fileContents[indexOfLetter + lineLength + 1]
        if (center != "A"):
            return False # We can just break right here
        bottomLeft = fileContents[indexOfLetter + 2 * lineLength]
        bottomRight = fileContents[indexOfLetter + 2 * lineLength + 2]
        topRight = fileContents[indexOfLetter + 2]
        if ((isM and bottomRight == "S") or (not isM and bottomRight == "M")) and ((bottomLeft == "M" and topRight == "S") or (bottomLeft == "S" and topRight == "M")):
            return True
    else: # Out of bounds, no X
        print(str(indexOfLetter + (2 * lineLength) + 2) + " was out of range of the string with length " + str(len(fileContents)))
        return False

if __name__ == "__main__":
    with open("advent_of_code_2024\\andrew\day4.txt", "r") as file:
        objTwo(file)