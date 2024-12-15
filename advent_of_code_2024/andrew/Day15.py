import os
import re
import copy

def objOne(fileContent: str):
    grid, instructions = re.split("\n\n", fileContent)
    directions = {"^": [-1, 0], ">": [0, 1], "v": [1, 0], "<": [0, -1]}

    grid = re.split("\n", grid) # now, it is an array of strings
    grid = [[f"{gridChar}" for gridChar in line] for line in grid] # now, it is a 2d array of characters
    startPosition = [0, 0]
    for line in range(len(grid)):
        for char in range(len(grid[line])):
            if grid[line][char] == "@":
                startPosition = [line, char]
    
    instructions = instructions.replace("\n", "")
    #print(instructions)

    step = 0
    for char in instructions:
        step += 1
        if grid[startPosition[0]+directions[char][0]][startPosition[1]+directions[char][1]] == ".": # If the spot its moving to is empty
            grid[startPosition[0]+directions[char][0]][startPosition[1]+directions[char][1]] = "@"
            grid[startPosition[0]][startPosition[1]] = "."
            startPosition[0] = startPosition[0]+directions[char][0]
            startPosition[1] = startPosition[1]+directions[char][1]
        elif grid[startPosition[0]+directions[char][0]][startPosition[1]+directions[char][1]] == "O": # If the spot is a box
            if moveBoxIfAllowed(grid, directions[char], startPosition):
                grid[startPosition[0]][startPosition[1]] = "."
                grid[startPosition[0]+directions[char][0]][startPosition[1]+directions[char][1]] = "@"
                #print(f"Shoved box, moved robot to {startPosition[0]+directions[char][0]},{startPosition[1]+directions[char][1]}")
                startPosition[0] = startPosition[0]+directions[char][0]
                startPosition[1] = startPosition[1]+directions[char][1]
            else:
                pass
                #print(f"Box was unmovable on step {step}")
        # Neither will trigger if it is a wall or if the box is unmovable
        '''
        print(f"Step {step}")

        for line in grid:
            for char in line:
                print(char, end="")
            print()
        print()'''
    
    gpsTotal = 0
    for line in range(len(grid)):
        for char in range(len(grid[line])):
            if grid[line][char] == "O":
                gpsTotal += line * 100 + char
    print(gpsTotal)

def moveBoxIfAllowed(grid: list, direction: list, robotPos: list) -> bool: # robotPos is row, col - returns True if succesful, False if not
    #directions = {"^": [-1, 0], ">": [0, 1], "v": [1, 0], "<": [0, -1]}
    # Is it in bounds? Is the tile PAST it in bounds as well? Otherwise you are trying to push a wall
    if (0 <= robotPos[0] + direction[0] < len(grid) and 0 <= robotPos[1] + direction[1] < len(grid[robotPos[0]])):
        # Tile PAST it:
        if (0 <= robotPos[0] + 2 * direction[0] < len(grid) and 0 <= robotPos[1] + 2 * direction[1] < len(grid[robotPos[0]])):
            # Now, check if its a box and if the next spot is empty (.)
            if grid[robotPos[0] + 2 * direction[0]][robotPos[1] + 2 * direction[1]] == "." and grid[robotPos[0]+direction[0]][robotPos[1]+direction[1]] == "O":
                # Swap them
                grid[robotPos[0] + 2 * direction[0]][robotPos[1] + 2 * direction[1]] = "O"
                grid[robotPos[0]][robotPos[1]] = "."
                return True
            # If it isn't empty, it could be another box. Check if you can move them both at once - 
            elif grid[robotPos[0] + 2 * direction[0]][robotPos[1] + 2 * direction[1]] == "O":
                if moveBoxIfAllowed(grid, direction, [robotPos[0] + direction[0], robotPos[1] + direction[1]]):
                    # Swap them
                    grid[robotPos[0] + 2 * direction[0]][robotPos[1] + 2 * direction[1]] = "O"
                    grid[robotPos[0]][robotPos[1]] = "."
                    return True
    return False

def canWideBoxMove(grid: list, direction: list, boxLeftPos: list) -> bool: # Basically a copy of moveWideBoxIfAllowed but it doesn't actually move things
    temp = copy.deepcopy(grid) # Python pisses me off SO MUCH because I have to do this to MODIFY A LIST WITHOUT MODIFYING THE INPUT LIST
    # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    didReturn = moveWideBoxIfAllowed(temp, direction, boxLeftPos)
    return didReturn

def moveWideBoxIfAllowed(grid: list, direction: list, boxLeftPos: list) -> bool:
    # Figure out if its sideways or up
    # I could write code for all directions at once, but I really want to understand what its doing, so
    # Check bounds for all of them, obviously, then split by direction:
    if (0 <= boxLeftPos[0]+direction[0] < len(grid) and 0 <= boxLeftPos[1]+direction[1] < len(grid[boxLeftPos[0]]) and 0 <= boxLeftPos[0]+direction[0]+1 < len(grid)):
        if direction == [0, 1]:
            if grid[boxLeftPos[0]][boxLeftPos[1]+2] == ".": # It is empty to the right
                grid[boxLeftPos[0]][boxLeftPos[1]] = "."
                grid[boxLeftPos[0]][boxLeftPos[1]+1] = "["
                grid[boxLeftPos[0]][boxLeftPos[1]+2] = "]"
                return True
            elif grid[boxLeftPos[0]][boxLeftPos[1]+2] == "[": # It is another box to the right
                if moveWideBoxIfAllowed(grid, direction, [boxLeftPos[0], boxLeftPos[1]+2]):
                    grid[boxLeftPos[0]][boxLeftPos[1]] = "."
                    grid[boxLeftPos[0]][boxLeftPos[1]+1] = "["
                    grid[boxLeftPos[0]][boxLeftPos[1]+2] = "]"
                    return True
        elif direction == [0, -1]:
            if grid[boxLeftPos[0]][boxLeftPos[1]-1] == ".":
                grid[boxLeftPos[0]][boxLeftPos[1]+1] = "."
                grid[boxLeftPos[0]][boxLeftPos[1]] = "]"
                grid[boxLeftPos[0]][boxLeftPos[1]-1] = "["
                return True
            elif grid[boxLeftPos[0]][boxLeftPos[1]-1] == "]":
                if moveWideBoxIfAllowed(grid, direction, [boxLeftPos[0], boxLeftPos[1]-2]):
                    grid[boxLeftPos[0]][boxLeftPos[1]+1] = "."
                    grid[boxLeftPos[0]][boxLeftPos[1]] = "]"
                    grid[boxLeftPos[0]][boxLeftPos[1]-1] = "["
                    return True
        elif direction == [-1, 0]:
            if grid[boxLeftPos[0]-1][boxLeftPos[1]] == "." and grid[boxLeftPos[0]-1][boxLeftPos[1]+1] == ".":
                grid[boxLeftPos[0]][boxLeftPos[1]] = "."
                grid[boxLeftPos[0]][boxLeftPos[1]+1] = "."
                grid[boxLeftPos[0]-1][boxLeftPos[1]] = "["
                grid[boxLeftPos[0]-1][boxLeftPos[1]+1] = "]"
                return True
            elif grid[boxLeftPos[0]-1][boxLeftPos[1]] == "[":
                if moveWideBoxIfAllowed(grid, direction, [boxLeftPos[0]-1, boxLeftPos[1]]):
                    grid[boxLeftPos[0]][boxLeftPos[1]] = "."
                    grid[boxLeftPos[0]][boxLeftPos[1]+1] = "."
                    grid[boxLeftPos[0]-1][boxLeftPos[1]] = "["
                    grid[boxLeftPos[0]-1][boxLeftPos[1]+1] = "]"
                    return True
            elif grid[boxLeftPos[0]-1][boxLeftPos[1]] == "]": # Now, the right could be empty OR another box
                if grid[boxLeftPos[0]-1][boxLeftPos[1]+1] == ".": # It's empty
                    if moveWideBoxIfAllowed(grid, direction, [boxLeftPos[0]-1, boxLeftPos[1]-1]):
                        grid[boxLeftPos[0]][boxLeftPos[1]] = "."
                        grid[boxLeftPos[0]][boxLeftPos[1]+1] = "."
                        grid[boxLeftPos[0]-1][boxLeftPos[1]] = "["
                        grid[boxLeftPos[0]-1][boxLeftPos[1]+1] = "]"
                        return True
                elif grid[boxLeftPos[0]-1][boxLeftPos[1]+1] == "[": # It's another box
                    # Now i've kinda hosed myself because wide box MOVES the box
                    # So I made a new method that just uses a copy
                    if canWideBoxMove(grid, direction, [boxLeftPos[0]-1, boxLeftPos[1]+1]) and canWideBoxMove(grid, direction, [boxLeftPos[0]-1, boxLeftPos[1]-1]):
                        moveWideBoxIfAllowed(grid, direction, [boxLeftPos[0]-1, boxLeftPos[1]+1])
                        moveWideBoxIfAllowed(grid, direction, [boxLeftPos[0]-1, boxLeftPos[1]-1])
                        grid[boxLeftPos[0]][boxLeftPos[1]] = "."
                        grid[boxLeftPos[0]][boxLeftPos[1]+1] = "."
                        grid[boxLeftPos[0]-1][boxLeftPos[1]] = "["
                        grid[boxLeftPos[0]-1][boxLeftPos[1]+1] = "]"
                        return True
            elif grid[boxLeftPos[0]-1][boxLeftPos[1]+1] == "[" and grid[boxLeftPos[0]-1][boxLeftPos[1]] == ".": # Finally, handle if there is just a right box
                if moveWideBoxIfAllowed(grid, direction, [boxLeftPos[0]-1, boxLeftPos[1]+1]):
                    grid[boxLeftPos[0]][boxLeftPos[1]] = "."
                    grid[boxLeftPos[0]][boxLeftPos[1]+1] = "."
                    grid[boxLeftPos[0]-1][boxLeftPos[1]] = "["
                    grid[boxLeftPos[0]-1][boxLeftPos[1]+1] = "]"
                    return True
        elif direction == [1, 0]:
            if grid[boxLeftPos[0]+1][boxLeftPos[1]] == "." and grid[boxLeftPos[0]+1][boxLeftPos[1]+1] == ".":
                grid[boxLeftPos[0]][boxLeftPos[1]] = "."
                grid[boxLeftPos[0]][boxLeftPos[1]+1] = "."
                grid[boxLeftPos[0]+1][boxLeftPos[1]] = "["
                grid[boxLeftPos[0]+1][boxLeftPos[1]+1] = "]"
                return True
            elif grid[boxLeftPos[0]+1][boxLeftPos[1]] == "[":
                if moveWideBoxIfAllowed(grid, direction, [boxLeftPos[0]+1, boxLeftPos[1]]):
                    grid[boxLeftPos[0]][boxLeftPos[1]] = "."
                    grid[boxLeftPos[0]][boxLeftPos[1]+1] = "."
                    grid[boxLeftPos[0]+1][boxLeftPos[1]] = "["
                    grid[boxLeftPos[0]+1][boxLeftPos[1]+1] = "]"
                    return True
            elif grid[boxLeftPos[0]+1][boxLeftPos[1]] == "]": # Now, the right could be empty OR another box
                if grid[boxLeftPos[0]+1][boxLeftPos[1]+1] == ".": # It's empty
                    if moveWideBoxIfAllowed(grid, direction, [boxLeftPos[0]+1, boxLeftPos[1]-1]):
                        grid[boxLeftPos[0]][boxLeftPos[1]] = "."
                        grid[boxLeftPos[0]][boxLeftPos[1]+1] = "."
                        grid[boxLeftPos[0]+1][boxLeftPos[1]] = "["
                        grid[boxLeftPos[0]+1][boxLeftPos[1]+1] = "]"
                        return True
                elif grid[boxLeftPos[0]+1][boxLeftPos[1]+1] == "[": # It's another box
                    # Now i've kinda hosed myself because wide box MOVES the box
                    # So I made a new method that just uses a copy
                    if canWideBoxMove(grid, direction, [boxLeftPos[0]+1, boxLeftPos[1]+1]) and canWideBoxMove(grid, direction, [boxLeftPos[0]+1, boxLeftPos[1]-1]):
                        moveWideBoxIfAllowed(grid, direction, [boxLeftPos[0]+1, boxLeftPos[1]+1])
                        moveWideBoxIfAllowed(grid, direction, [boxLeftPos[0]+1, boxLeftPos[1]-1])
                        grid[boxLeftPos[0]][boxLeftPos[1]] = "."
                        grid[boxLeftPos[0]][boxLeftPos[1]+1] = "."
                        grid[boxLeftPos[0]+1][boxLeftPos[1]] = "["
                        grid[boxLeftPos[0]+1][boxLeftPos[1]+1] = "]"
                        return True
            elif grid[boxLeftPos[0]+1][boxLeftPos[1]+1] == "[" and grid[boxLeftPos[0]+1][boxLeftPos[1]] == ".": # Finally, handle if there is just a right box
                if moveWideBoxIfAllowed(grid, direction, [boxLeftPos[0]+1, boxLeftPos[1]+1]):
                    grid[boxLeftPos[0]][boxLeftPos[1]] = "."
                    grid[boxLeftPos[0]][boxLeftPos[1]+1] = "."
                    grid[boxLeftPos[0]+1][boxLeftPos[1]] = "["
                    grid[boxLeftPos[0]+1][boxLeftPos[1]+1] = "]"
                    return True
    return False

def objTwo(fileContent: str):
    grid, instructions = re.split("\n\n", fileContent)
    directions = {"^": [-1, 0], ">": [0, 1], "v": [1, 0], "<": [0, -1]}

    # For objective 2, make everything wider:
    grid = grid.replace("#", "##")
    grid = grid.replace("O", "[]")
    grid = grid.replace(".", "..")
    grid = grid.replace("@", "@.")
    print("Step 0:")
    for line in grid:
        for char in line:
            print(char, end="")
    print("\n")
    grid = re.split("\n", grid) # now, it is an array of strings
    grid = [[f"{gridChar}" for gridChar in line] for line in grid] # now, it is a 2d array of characters
    startPosition = [0, 0]
    for line in range(len(grid)):
        for char in range(len(grid[line])):
            if grid[line][char] == "@":
                startPosition = [line, char]
    
    instructions = instructions.replace("\n", "")

    step = 0
    for char in instructions:
        step += 1
        if grid[startPosition[0]+directions[char][0]][startPosition[1]+directions[char][1]] == ".": # If the spot its moving to is empty
            grid[startPosition[0]+directions[char][0]][startPosition[1]+directions[char][1]] = "@"
            grid[startPosition[0]][startPosition[1]] = "."
            startPosition[0] = startPosition[0]+directions[char][0]
            startPosition[1] = startPosition[1]+directions[char][1]
        elif grid[startPosition[0]+directions[char][0]][startPosition[1]+directions[char][1]] == "[": # If the spot is the left half of a box
            if moveWideBoxIfAllowed(grid, directions[char], [startPosition[0]+directions[char][0], startPosition[1]+directions[char][1]]):
                grid[startPosition[0]][startPosition[1]] = "."
                grid[startPosition[0]+directions[char][0]][startPosition[1]+directions[char][1]] = "@"
                startPosition[0] = startPosition[0]+directions[char][0]
                startPosition[1] = startPosition[1]+directions[char][1]
                #print(f"Shoved box, moved robot to {startPosition[0]+directions[char][0]},{startPosition[1]+directions[char][1]}")
            else:
                pass
                #print(f"Box was unmovable on step {step}")
        elif grid[startPosition[0]+directions[char][0]][startPosition[1]+directions[char][1]] == "]":
            if moveWideBoxIfAllowed(grid, directions[char], [startPosition[0]+directions[char][0], startPosition[1]+directions[char][1]-1]):
                grid[startPosition[0]+directions[char][0]][startPosition[1]+directions[char][1]] = "@"
                grid[startPosition[0]][startPosition[1]] = "."
                startPosition[0] = startPosition[0]+directions[char][0]
                startPosition[1] = startPosition[1]+directions[char][1]
                #print(f"Shoved box, moved robot to {startPosition[0]+directions[char][0]},{startPosition[1]+directions[char][1]}")
            else:
                pass
                #print(f"Box was immovable on step {step}")
        # Neither will trigger if it is a wall or if the box is unmovable
        '''
        print(f"Step {step}")

        for line in grid:
            for char in line:
                print(char, end="")
            print()
        print()'''
    
    for line in grid:
        for char in line:
            print(char, end="")
        print()
    print()

    gpsTotal = 0
    for line in range(len(grid)):
        for char in range(len(grid[line])):
            if grid[line][char] == "[":
                gpsTotal += line * 100 + char
    print(gpsTotal)

with open(os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), "Day15.txt"), "r") as file:
    objTwo(file.read())