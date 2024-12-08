import re

class Antenna:
    def __init__(self, row, column, char) -> None:
        self.row = row
        self.col = column
        self.char = char
    def resPoint(self, otherAntenna) -> list: # Other antenna better be an Antenna, type hints don't like that though
        # If antenna 1 is at 3, 3 and antenna 2 is at 4, 4, antiNode if called on antenna 1 should be 2, 2 and antinode called on antenna 2 should be 5, 5
        return [self.row + self.row-otherAntenna.row, self.col + self.col-otherAntenna.col]
    def resPoints(self, otherAntenna, rowCount, colCount) -> list:
        returnArray = []
        counter = 1
        # On top of the normal line of antinodes, objTwo also wants you to count each antenna as a point
        returnArray.append([self.row, self.col])

        while 0 <= self.row + ((self.row-otherAntenna.row) * counter) < rowCount and 0 <= self.col + ((self.col-otherAntenna.col) * counter) < colCount:
            returnArray.append([self.row + ((self.row-otherAntenna.row)*counter), self.col + ((self.col-otherAntenna.col)*counter)])
            counter+=1
        return returnArray

def objOne(fileContent: str):
    lines = re.split("\n", fileContent)
    resonancePoints = [["." for i in range(len(lines[0]))] for j in range(len(lines))]
    antennaPoints = [["." for i in range(len(lines[0]))] for j in range(len(lines))]

    # Now, to fill in resonancePoints, we need to find every pair of antena on the same frequency
    # I made a custom antenna class just to make it a little easier to keep track of location

    # Also, dictionary to store antennas by char
    antennaDict = {}
    # It will be a dictionary with an array of antenna objects at each entry

    for i in range(48, 58, 1):
        antennaDict[chr(i)] = [] # '0' through '9'
    for i in range(60, 91, 1):
        antennaDict[chr(i)] = [] # 'A' through 'Z'
    for i in range(97, 123, 1):
        antennaDict[chr(i)] = []

    # First, find all antenas
    for line in range(len(lines)):
        for char in range(len(lines[line])):
            if lines[line][char] != ".":
                antennaDict[lines[line][char]].append(Antenna(row=line, column=char, char=lines[line][char]))
                antennaPoints[line][char] = lines[line][char]
    
    # Now, for every pair of antennas that are the same char, put in their resonance points
    for array in antennaDict.values():
        if len(array) > 1: # If it is only one antenna, there will be no antinodes
            for antenna in array: # For each antenna in the array, go through each OTHER antenna
                for otherAntenna in array:
                    if antenna != otherAntenna:
                        antinodeOne = antenna.resPoint(otherAntenna)
                        antinodeTwo = otherAntenna.resPoint(antenna)
                        # Check bounds on the returned values, and add if they are in bounds:
                        if 0 <= antinodeOne[0] < len(resonancePoints) and 0 <= antinodeOne[1] < len(resonancePoints[0]):
                            resonancePoints[antinodeOne[0]][antinodeOne[1]] = "#"
                        if 0 <= antinodeTwo[0] < len(resonancePoints) and 0 <= antinodeTwo[1] < len(resonancePoints[0]):
                            resonancePoints[antinodeTwo[0]][antinodeTwo[1]] = "#"
    
    for row in antennaPoints:
        for col in row:
            print(col, end="")
        print()
    print()
    antinodeCount = 0
    for row in resonancePoints:
        for col in row:
            if col == "#":
                antinodeCount += 1
            print(col, end="")
        print()

    print("Number of antinodes was " + str(antinodeCount))

# Yay, copying code! Obj 2 is very similar
def objTwo(fileContent: str):
    lines = re.split("\n", fileContent)
    resonancePoints = [["." for i in range(len(lines[0]))] for j in range(len(lines))]
    antennaPoints = [["." for i in range(len(lines[0]))] for j in range(len(lines))]

    # Now, to fill in resonancePoints, we need to find every pair of antena on the same frequency
    # I made a custom antenna class just to make it a little easier to keep track of location

    # Also, dictionary to store antennas by char
    antennaDict = {}
    # It will be a dictionary with an array of antenna objects at each entry

    for i in range(48, 58, 1):
        antennaDict[chr(i)] = [] # '0' through '9'
    for i in range(60, 91, 1):
        antennaDict[chr(i)] = [] # 'A' through 'Z'
    for i in range(97, 123, 1):
        antennaDict[chr(i)] = []

    # First, find all antenas
    for line in range(len(lines)):
        for char in range(len(lines[line])):
            if lines[line][char] != ".":
                antennaDict[lines[line][char]].append(Antenna(row=line, column=char, char=lines[line][char]))
                antennaPoints[line][char] = lines[line][char]
    
    # Now, for every pair of antennas that are the same char, put in their resonance points
    for array in antennaDict.values():
        if len(array) > 1: # If it is only one antenna, there will be no antinodes
            for antenna in array: # For each antenna in the array, go through each OTHER antenna
                for otherAntenna in array:
                    if antenna != otherAntenna:
                        antinodesOne = antenna.resPoints(otherAntenna, len(lines), len(lines[0]))
                        antinodesTwo = otherAntenna.resPoints(antenna, len(lines), len(lines[0]))
                        # No need to check bounds on the returned values, they were already checked this time:
                        for antinode in antinodesOne:
                            resonancePoints[antinode[0]][antinode[1]] = "#"
                        for antinode in antinodesTwo:
                            resonancePoints[antinode[0]][antinode[1]] = "#"
    
    for row in antennaPoints:
        for col in row:
            print(col, end="")
        print()
    print()
    antinodeCount = 0
    for row in resonancePoints:
        for col in row:
            if col == "#":
                antinodeCount += 1
            print(col, end="")
        print()

    print("Number of antinodes was " + str(antinodeCount))

if __name__ == "__main__":
    with open("advent_of_code_2024\\andrew\\Day8.txt", "r") as file:
        objTwo(file.read())