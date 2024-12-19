import os
from collections import defaultdict
import re
#from colorama import Fore, Back, Style
from sty import fg

# Custom class to store dijkstra's things
class DijkstraMap:
    def __init__(self) -> None:
        self.dict: dict[tuple] = defaultdict(lambda: [100000000000000, (None, None)]) # Hopefully this is large enough to not be an applicable answer
        # This dictionary will take the format of {(row, column, rowDirection, colDirection): [distance from START, (previous row, previous column)]}
    
    def get(self, element: tuple, direction: tuple) -> int:
        return self.dict[(element[0], element[1], direction[0], direction[1])][0] # The distance from the START to this
    
    def set(self, element: tuple, direction: tuple, distance: int, prev: tuple) -> None:
        if self.dict[(element[0], element[1], direction[0], direction[1])][0] > distance:
            self.dict[(element[0], element[1], direction[0], direction[1])] = [distance, prev]

    def getPrev(self, element: tuple, direction: tuple) -> tuple:
        # There is no reason to have this in a mathod specifically, just for convention
        return self.dict[(element[0], element[1], direction[0], direction[1])][1]

    def buildDistances(self, grid: list[str], startCoords: tuple) -> None:

        alreadyCompleted: set = set([]) # Both unordered because it doesn't go in one contiguous path - it just goes until every node has been visited
        yetToComplete: set = set([])

        # We put the start node in yetToBeComplete so we start with it and slowly add its neighbors
        yetToComplete.add((startCoords[0], startCoords[1], 0, 1))
        self.set(startCoords, (0, 1), 0, (None, None))

        """
        for line in range(len(grid)):
            for char in range(len(grid[line])):
                if grid[line][char] == ".":
                    yetToComplete.add((line, char)) # Thus, yetToComplete is the set of all nodes to start
        """

        #print(grid)

        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        loopCount = 0

        # We're doing distance from the start, so having startCoords is important
        while len(yetToComplete) > 0:
            loopCount += 1
            #print(len(yetToComplete))
            # When starting, this nextElement will be the start. Otherwise, it could be anywhere
            # However, there is always the guarentee that it was reached by a previous path
            nextElement = yetToComplete.pop()
            # Now, we set values of all of this node's possible neighbors
            for dir in directions:
                if 0 <= nextElement[0]+dir[0] < len(grid) and 0 <= nextElement[1]+dir[1] < len(grid[0]) and grid[nextElement[0]+dir[0]][nextElement[1]+dir[1]] in [".", "E"]: # So we also get the end
                    # Now, we need to find what the cost to this neighbor is

                    directionOfBefore = [nextElement[2], nextElement[3]]

                    costToUpdate = None
                    if dir != directionOfBefore: # If its turning
                        if (dir[0] == directionOfBefore[0]) or (dir[1] == directionOfBefore[1]): # Then, they are 180 degree opposed - thus, we can't get to this node
                            costToUpdate = None # Turning, but impossible - maybe
                        else: 
                            costToUpdate = 1001 # Turning, but possible
                    else:
                        costToUpdate = 1 # Not turning
                    
                    # The element in this direction is a node we can route to, so update its path if this way is close than what it is
                    # The setter method checks this, so we can just call that method
                    if costToUpdate != None:
                        self.set((nextElement[0]+dir[0],nextElement[1]+dir[1]), self.get(nextElement)+costToUpdate, nextElement) # Cost from start to previous node + cost to this node
                        if not ((nextElement[0]+dir[0],nextElement[1]+dir[1], dir[0], dir[1]) in yetToComplete or (nextElement[0]+dir[0],nextElement[1]+dir[1], dir[0], dir[1]) in alreadyCompleted):
                            if grid[nextElement[0]+dir[0]][nextElement[1]+dir[1]] != "E": # Also make sure this isn't the end - don't move PAST the end
                                print(f"Added node {nextElement[0]+dir[0]},{nextElement[1]+dir[1]} from direction {dir}")
                                yetToComplete.add((nextElement[0]+dir[0],nextElement[1]+dir[1], dir[0], dir[1]))
            alreadyCompleted.add(nextElement)

def objOne(fileContent: str):
    lines = re.split("\n", fileContent)
    startCoords = (0, 0)
    endCoords = (0, 0)
    for line in range(len(lines)):
        if lines[line].count('S') != 0:
            startCoords = (line, lines[line].index('S'))
        elif lines[line].count('E') != 0:
            endCoords = (line, lines[line].index('E'))

    coordMap = DijkstraMap()
    coordMap.buildDistances(lines, startCoords)
    endDist = 10000000000
    for dir in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        if coordMap.get(endCoords, dir) < endDist:
            endDist = coordMap.get(endCoords, dir)
        else:
            print(coordMap.get(endCoords, dir))

    for line in range(len(lines)):
        for char in range(len(lines[line])):
            if lines[line][char] == "#":
                print(fg(255, 255, 255) + '#  ', end="")
            #if not (((line, char) in solutionSet) or ((line, char) in testSet)):
            #    print(fg(255, 255, 255) + lines[line][char] + " ", end=" ")
            else:
                cap = 5000
                colorTerm = fg(255, 255, 255)
                posScore = coordMap.get((line, char), (-1, 0))
                colorTerm = fg(int(posScore / (cap/255)) % 255, 100, 255 - int(posScore / (cap/255)) % 255)
                if ((line, char) == endCoords):
                    colorTerm = fg(0, 255, 0)
                print(colorTerm + str(posScore)[-1:], end="  ")
        print()
    
    print(endDist)
    #print(coordMap.get(testElement))

with open(os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), "Day16.txt"), "r") as file:
    objOne(file.read())