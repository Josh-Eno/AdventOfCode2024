import doctest
import re

class Edge:
    def __init__(self, beginRow: int, beginColumn: int, length: int, dir: bool): # Direction is True if horizontal
        self.row = beginRow
        self.col = beginColumn
        self.length = length
        self.horiz = dir
    def __str__(self):
        return f"({self.row},{self.col}) -- {self.length}"
    
    def toTuple(self) -> tuple[int, int, int, bool]: # Returns a tuple of (row, col, len, dir)
        return (self.row, self.col, self.length, self.horiz)
    
    def __hash__(self):
        return self.row*self.col*self.length*(1 if self.horiz else 2)

class PlotSet:
    def __init__(self, symbol) -> None:
        self.symbol = symbol
        self.signature = f"0:0:{symbol}" # Area:Perimiter:Symbol, The unique identifier of the plot, based on area, perimiter, and symbol (we assume that the areas and perimeters of other plots with the same symbols are probably different)
        self.coordSet = set([]) # Contains every tile in the plot, [[Row, Column],]
        self.perimeter = 0 # Set of perimiter tiles so i don't count DUPLICATES
        self.diagons = set([])
        self.edges = set([])

    def addTile(self, linesArr: list[int], row: int, col: int) -> None:
        self.coordSet.add((row, col))
        # Edges are already added, so

    def addTileAndNeighbors(self, linesArr: list[str], startRow: int, startCol: int) -> None: # This is where we propogate the search
        directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        # Check that the neighbor is in bounds of the line / column AND that its symbol is the same for each direction
        neighborsInSet = [] # For perimeter
        neighborsToBeAdded = [] # For adding neighbors to the set
        for direction in directions:
            if (0 <= startRow+direction[0] < len(linesArr) and 0 <= startCol+direction[1] < len(linesArr[startRow+direction[0]])):
                neighborsInSet.append(linesArr[startRow+direction[0]][startCol+direction[1]] == self.symbol)
                if (not self.isInSet(startRow + direction[0], startCol + direction[1])) and (linesArr[startRow + direction[0]][startCol + direction[1]] == self.symbol):
                    neighborsToBeAdded.append([startRow + direction[0], startCol + direction[1]])
            else:
                self.edges.add(Edge(startRow+direction[0], startCol+direction[1], 1, True if (direction == [-1, 0] or direction == [1, 0]) else False))
                neighborsInSet.append(False)
       # print("Tile (" + str(startRow) + ", " + str(startCol) + ") was added with a perimiter of " + str(neighborsInSet.count(False)))
        self.addTile(linesArr, startRow, startCol)
        for tile in neighborsToBeAdded:
            self.addTileAndNeighbors(linesArr, tile[0], tile[1])
    
    def isInSet(self, row: int, col: int) -> bool:
        return (row, col) in self.coordSet
    
    def unionEdges(self, edge1: Edge, edge2: Edge) -> Edge: # Returns None if it can't
        # Determine if edges are next to each other and in line
        # If they aren't, you can't union them, so return false
        if (edge1.row == edge2.row and edge1.horiz == True and edge2.horiz == True):
            if abs(edge1.col-edge2.col) == 1: # It really shouldn't be zero, but just in case
                # Return the one with the lowest col number 
                colNum = edge1.col if edge1.col < edge2.col else edge2.col
                length = edge1.length + 1 if edge1.length > edge2.length else edge2.length + 1
                return Edge(edge1.row, colNum, length, True)
        elif (edge1.col == edge2.col and edge1.horiz == False and edge2.horiz == False):
            if abs(edge1.row-edge2.row) <= 1:
                rowNum = edge1.row if edge1.row < edge2.row else edge2.row
                length = edge1.length + 1 if edge1.length > edge2.length else edge2.length + 1
                return Edge(rowNum, edge1.col, length, False)
        else: # They have no common axis, thus are either diagonals or far apart from each other and should be counted seperately or unioned later
            return None

    def calcPerimeterEdges(self): # innefficient as heck but if it works it works
        # I really just wanna be done with today, so
        edgeArray = list(self.edges)
        failed = True
        while failed:
            failedThisLoop = False
            for i in range(len(edgeArray)):
                for j in range(len(edgeArray)): # Try to union current edge (edgeArray[i]) with every other edge
                    if (i != j):
                        returnVal = self.unionEdges(edgeArray[i], edgeArray[j])
                        if returnVal != None:
                            print("Unioned " + str(edgeArray[i]) + " and " + str(edgeArray[j]))
                            edgeArray.pop(j)
                            edgeArray.pop(i)
                            edgeArray.insert(i, returnVal)
                            failedThisLoop = True
                            break # Break out of the for loop, redo the while loop
                if failedThisLoop:
                    break
            if not failedThisLoop: # Went through all edges and couldn't union any
                failed = False
        self.edges = set(edgeArray)

    def price(self, linesArr) -> int:
        # Fill out perimeter set

        # Must bounds check for perimiter to be able to check if it is a tile:
        directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        diagonalDirections = [[-1, -1], [-1, 1], [1, 1], [1, -1]]
        for tile in self.coordSet:
            perimeterFoundOnSide = [False, False, False, False] # For objective 2
            directionIndex = 0
            for direction in directions:
                if (0 <= tile[0]+direction[0] < len(linesArr) and 0 <= tile[1]+direction[1] < len(linesArr[tile[0]+direction[0]])) and linesArr[tile[0]+direction[0]][tile[1]+direction[1]] != self.symbol: # If you can check its symbol and it isn't this set's symbol
                    perimeterFoundOnSide[directionIndex] = True
                    self.edges.add(Edge(tile[0]+direction[0], tile[1]+direction[1], 1, (True if (direction == [-1, 0] or direction == [1, 0]) else False)))
                elif not (0 <= tile[0]+direction[0] < len(linesArr) and 0 <= tile[1]+direction[1] < len(linesArr[tile[0]+direction[0]])): # If its past the bounds
                    self.edges.add(Edge(tile[0]+direction[0], tile[1]+direction[1], 1, (True if (direction == [-1, 0] or direction == [1, 0]) else False)))
                    perimeterFoundOnSide[directionIndex] = True
                directionIndex += 1

            # This is the nasty part, lots of ifs (as if the rest of the code isn't nasty too, lol)
            # If it is entirely corners...
            outsideCorners = 0
            if (perimeterFoundOnSide[0] and perimeterFoundOnSide[1] and perimeterFoundOnSide[2] and perimeterFoundOnSide[3]):
                outsideCorners += 4
            # Now if it has at least two corners in one tile, it means another corner... 
            elif (perimeterFoundOnSide[0] and perimeterFoundOnSide[1] and perimeterFoundOnSide[2]) or (perimeterFoundOnSide[1] and perimeterFoundOnSide[2] and perimeterFoundOnSide[3]) or (perimeterFoundOnSide[0] and perimeterFoundOnSide[2] and perimeterFoundOnSide[3]) or (perimeterFoundOnSide[1] and perimeterFoundOnSide[0] and perimeterFoundOnSide[3]):
                outsideCorners += 2
            # If it has one corner...
            elif (perimeterFoundOnSide[0] and perimeterFoundOnSide[1]) or (perimeterFoundOnSide[1] and perimeterFoundOnSide[2]) or (perimeterFoundOnSide[2] and perimeterFoundOnSide[3]) or (perimeterFoundOnSide[3] and perimeterFoundOnSide[0]):
                outsideCorners += 1

            # Now, check for inside corners
            values = [".", ".", ".", ".", ".", ".", ".", ".", "."]
            dirs = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1]]
            for i in range(9):
                if 0 <= tile[0]+dirs[i][0] < len(linesArr) and 0 <= tile[1]+dirs[i][1] < len(linesArr[tile[0]+dirs[i][0]]):
                    values[i] = linesArr[tile[0]+dirs[i][0]][tile[1]+dirs[i][1]]

            # Shamelessly using somebody elses code (chatgpt ;) )
            # List of conditions for inside corners
            # The order of values is - TopLeft-0, Top-1, TopRight-2, Left-3, Center-4, Right-5, BottomLeft-6, Bottom-7, BottomRight-8 
            inside_conditions = [
                (values[3] == self.symbol and values[1] == self.symbol and values[0] != self.symbol),
                (values[1] == self.symbol and values[5] == self.symbol and values[2] != self.symbol),
                (values[5] == self.symbol and values[7] == self.symbol and values[8] != self.symbol),
                (values[7] == self.symbol and values[3] == self.symbol and values[6] != self.symbol)
            ]
            insideCorners = sum(1 for condition in inside_conditions if condition)
            self.perimeter += outsideCorners + insideCorners

        #self.perimeter = 0
        #self.calcPerimeterEdges()

        #workaroundSet: set = set([])
        #for edge in self.edges:
        #    workaroundSet.add(edge.toTuple())

        #self.perimeter = len(workaroundSet)

        #print(workaroundSet)

        return len(self.coordSet) * self.perimeter

def objOne(fileContent: str) -> None:
    allPlots: list[PlotSet] = []
    lines = re.split("\n", fileContent)
    print("Going through all tiles...")
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            inAPlot = False
            plotIndex = 0
            while not inAPlot and plotIndex < len(allPlots):
                if allPlots[plotIndex].isInSet(row, col):
                    inAPlot = True
                    break
                plotIndex += 1
            if inAPlot:
                #print("Tile (" + str(row) + ", " + str(col) + ") was in a plot already!")
                continue
            else:
                newPlot = PlotSet(lines[row][col])
                newPlot.addTileAndNeighbors(lines, row, col)
                allPlots.append(newPlot)
    print("Printing price..., there are " + str(len(allPlots)) + " plots.")
    totalPrice = 0
    for plot in allPlots:
        totalPrice += plot.price(lines)
    print(totalPrice)
    '''
    print("Printing tiles...")
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            inAPlot = False
            plotIndex = 0
            while not inAPlot and plotIndex < len(allPlots):
                if allPlots[plotIndex].isInSet(row, col):
                    inAPlot = True
                    break
                plotIndex += 1
            print(allPlots[plotIndex].symbol, end="")
        print()
    print()'''
    #print("Printing edges... Edges are: ")

    #for plot in allPlots:
    #    print("Plot " + str(plot.symbol) + " had an area of " + str(len(plot.coordSet)) + " and a perimeter of " + str(plot.perimeter))

if __name__ == "__main__":
    doctest.testmod()
    with open("advent_of_code_2024\\andrew\\Day12.txt", "r") as file:
        objOne(file.read())