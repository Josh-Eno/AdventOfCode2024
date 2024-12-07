import re
import time
import multiprocessing

def objOne(fileContent: str) -> int:
    lines = re.split("\n", fileContent)
    linesArray = [list(lines[i][j] for j in range(len(lines[0]))) for i in range(len(lines))]
    startPosition = [0, 0]
    for line in range(len(linesArray)):
        for i in range(len(linesArray[line])):
            if linesArray[line][i] == "^":
                startPosition = [line, i]
    #print(startPosition)
    # Now, perform stepping
    position = startPosition
    incomplete = True
    # (0 < position[0] < len(lines)) and (0 < position[1] < len(lines[0]))
    charToDirection = {
        "^": [-1, 0],
        ">": [0, 1],
        "v": [1, 0],
        "<": [0, -1]
    }
    chars = ["^", ">", "v", "<"]
    count = 0
    #print("Lines has " + str(len(lines)) + " lines and each is a length of " + str(len(lines[0])))
    while incomplete: # While position is in bounds, follow direction and then rotate or mark incomplete
        char = linesArray[position[0]][position[1]] # Make sure to get the char
        directionToGo = charToDirection[char]
        bonk = linesArray[position[0] + directionToGo[0]][position[1] + directionToGo[1]] == "#" # Self explanitory I hope
        while bonk == False and (0 <= position[0] + directionToGo[0] < len(linesArray)) and (0 <= position[1] + directionToGo[1] < len(linesArray[0])):
            #print("At index " + str(position))
            linesArray[position[0]][position[1]] = "X" # Set position to X
            count += 1
            position[0] = position[0] + directionToGo[0] # Move position forward
            position[1] = position[1] + directionToGo[1]
            linesArray[position[0]][position[1]] = char # Put char at new position
            # Check position after this new position
            if (0 <= position[0] + directionToGo[0] < len(linesArray)) and (0 <= position[1] + directionToGo[1] < len(linesArray[0])):
                bonk = linesArray[position[0] + directionToGo[0]][position[1] + directionToGo[1]] == "#"
            else:
                linesArray[position[0]][position[1]] = "X"
                incomplete = False
        if not ((position[0] + directionToGo[0] < len(lines)) and (position[1] + directionToGo[1] < len(lines[0]))):
            linesArray[position[0]][position[1]] = "X"
            incomplete = False
        # Bonk was true, so now we turn right
        # Find char in chars
        charIndex = 0
        for i in range(len(chars)):
            if char == chars[i]:
                charIndex = i
                break
        # Make the char at final position be turned to the right
        linesArray[position[0]][position[1]] = chars[(charIndex + 1 if charIndex < 3 else 0)]
    count = 0
    for line in linesArray:
        for char in line:
            if char in ["X", "^", ">", "<", "v"]:
                count += 1 # Dunno why the other count didn't work
            #print(char, end="")
        #print("")
    #print(count)
    return count

def isLoop(linesArrayParam: list, debug=False) -> bool:
    # THIS FUNCTION SHOULD NEVER INFINITELY LOOP
    # IT LITERALLY DETECTS LOOPS AS IT GOES
    isLooping = False

    linesToModify = list(linesArrayParam).copy()

    charToDirection = {
        "^": [-1, 0],
        ">": [0, 1],
        "v": [1, 0],
        "<": [0, -1]
    }
    chars = ["^", ">", "v", "<"]

    position = [0, 0]

    for line in range(len(linesToModify)):
        for i in range(len(linesToModify[line])):
            if linesToModify[line][i] == "^":
                position = [line, i]

    if debug:
        print("Starting at " + str(position))

    currentChar = "^"
    currentCharIndex = 0

    exitCount = 0

    while not isLooping:
        exitCount += 1
        if exitCount > len(linesToModify)*len(linesToModify):
            return True
        # Follow the directions, if you encounter your own tracks and are moving in the same direction, then you are looping.
        # Using custom characters to mark tracks: U is up, R is right, D is down, L is left
        direction = charToDirection[currentChar]
        if debug:
            print("Direction is " + str(direction))
            print("X constraints are 0 <= " + str(position[0] + direction[0]) + " < " + str(len(linesToModify)))
            print("Y constraints are 0 <= " + str(position[1] + direction[1]) + " < " + str(len(linesToModify[0])))
        # Is the next move in-bounds?
        if (0 <= position[0] + direction[0] < len(linesToModify)) and (0 <= position[1] + direction[1] < len(linesToModify[0])):
            if debug:
                print("Running if part of loop")
            pathChar = linesToModify[position[0] + direction[0]][position[1] + direction[1]]
            bonk = pathChar == "#"
            if bonk:
                if debug:
                    print("Rotating")
                currentCharIndex = (currentCharIndex + 1 if currentCharIndex < 3 else 0)
                currentChar = chars[currentCharIndex]
            elif pathChar in ["U", "R", "D", "L"]:
                if debug:
                    print("\nRan across a path\n")
                if (pathChar == "U" and currentChar == "^") or (pathChar == "R" and currentChar == ">") or (pathChar == "D" and currentChar == "v") or (pathChar == "L" and currentChar == "<"):
                    return True
                elif (0 <= position[0] + direction[0] * 2 < len(linesToModify)) and (0 <= position[1] + direction[1] * 2 < len(linesToModify[0])) and (linesToModify[position[0] + direction[0] * 2][position[1] + direction[1] * 2] == "#"):
                    # Check if one ahead of pathchar is an obstacle and thus, it WILL turn into that path when it hits the obstacle
                    if (pathChar == "U" and currentChar == "<") or (pathChar == "R" and currentChar == "^") or (pathChar == "D" and currentChar == ">") or (pathChar == "L" and currentChar == "v"):
                        return True
                if debug:
                    print("Path didn't result in anything, continuing")
                # Proceed across the path as usual v, since it didn't satisfy any loop conditions
            if not bonk: # No bonk and no loops, continue
                if debug:
                    print("Going forward to " + str([position[0] + direction[0], position[1] + direction[1]]))
                linesToModify[position[0] + direction[0]][position[1] + direction[1]] = currentChar
                charLeftBehind = ("U" if currentChar == "^" else ("R" if currentChar == ">" else ("D" if currentChar == "v" else "L"))) # ick
                linesToModify[position[0]][position[1]] = charLeftBehind
                position[0] = position[0] + direction[0]
                position[1] = position[1] + direction[1]
        else:
            if debug:
                print("Running else part of loop")
            return False # It hit an edge, so obv it isn't looping

def objTwo(fileContent: str) -> None:
    # Get the lines into an array to modify
    lines = re.split("\n", fileContent)
    linesArray = [list(lines[i][j] for j in range(len(lines[0]))) for i in range(len(lines))]
    # Count of how many situations looped infinitely
    count = 0
    startLocation = [0, 0]

    for line in range(len(linesArray)):
        for i in range(len(linesArray[line])):
            if linesArray[line][i] == "^":
                startLocation = [line, i]

    # Loop through every possible place you can put an obstacle

    for row in range(len(linesArray)):
        for column in range(len(linesArray[0])):
            if (linesArray[row][column] == "."):
                temp = linesArray[row][column]
                linesArray[row][column] = "#" # Add the obstacle

                '''
                for line in linesArray:
                    for char in line:
                        print(char, end="")
                    print("")
                print("")
                '''

                count += 1 if isLoop(linesArray) else 0

                linesArray[row][column] = temp # Undo the obstacle? Despite it being a copy?? Python, why are you like this????
            for lineIndex in range(len(linesArray)):
                for charIndex in range(len(linesArray[lineIndex])):
                    if linesArray[lineIndex][charIndex] in ["U", "R", "D", "L", "^", ">", "v", "<"]:
                        linesArray[lineIndex][charIndex] = "." # Because GOD FORBID A COPY WORKS PYTHON
            linesArray[startLocation[0]][startLocation[1]] = "^"

        print("Got through row " + str(row) + " out of " + str(len(linesArray)))
    print(count)

    #print("Now evaluating a specific graph")
    #copy = linesArray.copy()
    #copy[6][3] = "#"
    #print(isLoop(copy, debug=True))

def constructStringFromArray(arr: list) -> str:
    returnString = ""
    for line in arr:
        if returnString != "":
            returnString += "\n"
        for char in line:
            returnString += char
    return returnString

if __name__ == "__main__":
    with open("advent_of_code_2024\\andrew\\Day6.txt", "r") as file:
        objTwo(file.read())