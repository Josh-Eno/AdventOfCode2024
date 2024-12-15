import re
import math
import os
import time

def objOne(fileContent: str):
    lines = re.split("\n", fileContent)
    x = 101
    y = 103
    finalGrid = [[0 for _ in range(x)] for _ in range(y)]
    for line in lines:
        startPos = [int(re.split(",", re.split(" ", line)[0])[0][2:]), int(re.split(",", re.split(" ", line)[0])[1])] # Ugly but works - could also do it based on line.index("=") and line.index(" ")
        vel = [int(re.split(",", re.split(" ", line)[1])[0][2:]), int(re.split(",", re.split(" ", line)[1])[1])]
        # [0] is the column, [1] is the row
        
        # Time jump is 100 seconds:
        timeJump = 100
        finalPos = [(vel[1] * timeJump + startPos[1]) % y, (vel[0] * timeJump + startPos[0]) % x]
        finalGrid[finalPos[0]][finalPos[1]] += 1
    
    # Now count the robots per quadrant
    quadrants = [0, 0, 0, 0]
    
    #print(f"The end of quad 1 was {math.floor(y / 2)}, {math.floor(x / 2)}")
    #print(f"The start of quad 3 is {math.ceil(y / 2)}, {math.ceil(x / 2)}")

    for row in range(y):
        for column in range(x):
            if row < math.floor(y / 2): # Quadrant 1 or 2
                if column < math.floor(x / 2):
                    quadrants[0] += finalGrid[row][column]
                elif column >= math.ceil(x / 2):
                    quadrants[1] += finalGrid[row][column]
            elif row >= math.ceil(y / 2): # Quadrant 3 or 4
                if column < math.floor(x / 2): # Quadrant 3
                    quadrants[2] += finalGrid[row][column]
                elif column >= math.ceil(x / 2): # Quadrant 4
                    quadrants[3] += finalGrid[row][column]

    #print("The safety factor is " + str(quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]))

def objTwo(fileContent: str):
    for timeJump in range(10404):
        lines = re.split("\n", fileContent)
        x = 101
        y = 103
        finalGrid = [[0 for _ in range(x)] for _ in range(y)]
        for line in lines:
            startPos = [int(re.split(",", re.split(" ", line)[0])[0][2:]), int(re.split(",", re.split(" ", line)[0])[1])] # Ugly but works - could also do it based on line.index("=") and line.index(" ")
            vel = [int(re.split(",", re.split(" ", line)[1])[0][2:]), int(re.split(",", re.split(" ", line)[1])[1])]
            # [0] is the column, [1] is the row
            
            finalPos = [(vel[1] * timeJump + startPos[1]) % y, (vel[0] * timeJump + startPos[0]) % x]
            finalGrid[finalPos[0]][finalPos[1]] += 1
        
        # If it seems to be maybe a christmas tree, print it

        if evaluateGridForTree(finalGrid):
            print(f"Second {timeJump}\n")
            # Condense by only printing every other line
            even = False
            for lin in finalGrid:
                if even:
                    even = False
                    continue
                else:
                    for char in lin:
                        if char != 0:
                            print(char, end="")
                        else:
                            print(".", end="")
                    even = True
                print()
        
        if timeJump % 1000 == 0:
            print(f"Timejump is {timeJump}")
        
def evaluateGridForTree(grid: list):
    # Try if it has, say, 4 robots next to each other
    
    foundDiagonals = False
    for row in range(len(grid)):
        for char in range(len(grid[row])):
            threshold = 6 # Require 4 diagonals to be found to be successful
            downAndRight = 0
            downAndLeft = 0
            downAndRightMatches = 0
            downAndLeftMatches = 0
            while downAndRight < threshold and 0 <= row + downAndRight < len(grid) and 0 < char + downAndRight < len(grid[row]):
                if grid[row][char] == grid[row - downAndRight][char + downAndRight] and grid[row][char] != 0:
                    downAndRightMatches += 1
                downAndRight += 1
            # Do the same for downAndLeft
            while (downAndRightMatches + downAndLeft) < threshold and 0 < row + downAndLeft < len(grid) and 0 < char - downAndLeft < len(grid[row]):
                if grid[row][char] == grid[row + downAndLeft][char -downAndLeft] and grid[row][char] != 0:
                    downAndLeftMatches += 1
                downAndLeft += 1

            if downAndRightMatches + downAndLeftMatches >= threshold:
                foundDiagonals = True
    
    return foundDiagonals

    '''
    # Instead, just average all of their positions:
    count = 0
    xPos = 0
    yPos = 0
    xSquaredPos = 0
    ySquaredPos = 0
    for row in range(len(grid)):
        for char in range(len(grid[row])):
            if char != 0:
                xPos += char
                # This needs to be fixed so its squared distance from *the center*
                xSquaredPos += char*char
                yPos += row
                ySquaredPos += row*row
                count += char # In case there is multiple robots

    thresh = 0.02 # Average is within 60% of the center - thats a weird way to put it, but basically there will be (1 - thresh) / 2 percent of the bounds on each side - 20% in this case
    x = 101
    y = 103
    center = [math.ceil(x / 2), math.ceil(y / 2)]

    withinThreshX = False
    withinThreshY = False
    if thresh * center[0] < (xPos / count) < (thresh + 1) * center[0]:
        withinThreshX = True
    if thresh * center[1] < (yPos / count) < (thresh + 1) * center[1]:
        withinThreshY = True
    
    if withinThreshY and withinThreshX:
        return True

    return False
    '''

with open(os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), "Day14.txt"), "r") as file:
    objTwo(file.read())