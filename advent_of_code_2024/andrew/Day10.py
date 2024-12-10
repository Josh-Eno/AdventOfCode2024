import re
import doctest

class Graph:
    def __init__(self, linesArray):
        self.lines = list([list(map(int, linesArray[i])) for i in range(len(linesArray))])
        self.trailheads = []
        self.peaks = []
        for lineIndex in range(len(self.lines)):
            for charIndex in range(len(self.lines[lineIndex])):
                if self.lines[lineIndex][charIndex] == 0:
                    self.trailheads.append([lineIndex, charIndex])
                elif self.lines[lineIndex][charIndex] == 9:
                    self.peaks.append([lineIndex, charIndex])
        print("Trailheads: " + str(self.trailheads))
        print("Peaks: " + str(self.peaks))
    
    def computeTrailheadScores(self) -> int:
        sumOfScores = 0
        for trailhead in self.trailheads:
            # Compute the number of paths
            numberOfPaths = 0
            for peak in self.peaks:
                # It doesn't matter how many different paths there are to the peak
                numberOfPaths += 1 if self.doesPathExist(trailhead[0], trailhead[1], peak[0], peak[1]) else 0
            sumOfScores += numberOfPaths
        return sumOfScores
    
    def computeTrailheadScores2(self) -> int:
        sumOfScores = 0
        for trailhead in self.trailheads:
            # Compute the number of paths
            numberOfPaths = 0
            for peak in self.peaks:
                numberOfPaths += self.howManyPathsExist(trailhead[0], trailhead[1], peak[0], peak[1])
            sumOfScores += numberOfPaths
        return sumOfScores
    
    def doesPathExist(self, startRow, startCol, targetRow, targetCol) -> bool:
        # Recursion might make this terrible BUT I don't want to do any actaul pathfinding so...
        startValue = self.lines[startRow][startCol]
        foundPath = False
        if 0 <= startRow-1 < len(self.lines) and self.lines[startRow-1][startCol] == startValue + 1:
            foundPath = (self.doesPathExist(startRow-1, startCol, targetRow, targetCol) if not (startRow-1 == targetRow and startCol == targetCol) else True)
        if 0 <= startCol+1 < len(self.lines[startRow]) and self.lines[startRow][startCol+1] == startValue + 1 and not foundPath:
            foundPath = (self.doesPathExist(startRow, startCol+1, targetRow, targetCol) if not (startRow == targetRow and startCol+1 == targetCol) else True)
        if 0 <= startRow+1 < len(self.lines) and self.lines[startRow+1][startCol] == startValue + 1 and not foundPath:
            foundPath = (self.doesPathExist(startRow+1, startCol, targetRow, targetCol) if not (startRow+1 == targetRow and startCol == targetCol) else True)
        if 0 <= startCol-1 < len(self.lines[startRow]) and self.lines[startRow][startCol-1] == startValue + 1 and not foundPath:
            foundPath = (self.doesPathExist(startRow, startCol-1, targetRow, targetCol) if not (startRow == targetRow and startCol-1 == targetCol) else True)
        
        return foundPath
    
    def howManyPathsExist(self, startRow, startCol, targetRow, targetCol) -> int:
        startValue = self.lines[startRow][startCol]
        foundPaths = 0
        if 0 <= startRow-1 < len(self.lines) and self.lines[startRow-1][startCol] == startValue + 1:
            foundPaths += (self.howManyPathsExist(startRow-1, startCol, targetRow, targetCol) if not (startRow-1 == targetRow and startCol == targetCol) else 1)
        if 0 <= startCol+1 < len(self.lines[startRow]) and self.lines[startRow][startCol+1] == startValue + 1:
            foundPaths += (self.howManyPathsExist(startRow, startCol+1, targetRow, targetCol) if not (startRow == targetRow and startCol+1 == targetCol) else 1)
        if 0 <= startRow+1 < len(self.lines) and self.lines[startRow+1][startCol] == startValue + 1:
            foundPaths += (self.howManyPathsExist(startRow+1, startCol, targetRow, targetCol) if not (startRow+1 == targetRow and startCol == targetCol) else 1)
        if 0 <= startCol-1 < len(self.lines[startRow]) and self.lines[startRow][startCol-1] == startValue + 1:
            foundPaths += (self.howManyPathsExist(startRow, startCol-1, targetRow, targetCol) if not (startRow == targetRow and startCol-1 == targetCol) else 1)
        
        return foundPaths
        
def objOne(fileContent: str):
    graph = Graph(re.split("\n", fileContent))
    print(graph.computeTrailheadScores())

def objTwo(fileContent: str):
    graph = Graph(re.split("\n", fileContent))
    print(graph.computeTrailheadScores2())

if __name__ == "__main__":
    with open("advent_of_code_2024\\andrew\\Day10.txt", "r") as file:
        objTwo(file.read())