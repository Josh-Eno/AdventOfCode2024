import doctest
import sympy
import re
import math

def coefficientsManually(firstVec, secondVec, resultVec) -> list[int, int]:
    # We need two equations of the form:
    # 1: a1*x + b1*y = c1:
    # 2: a2*x + b2*y = c2
    # With x being button 1 presses and y being button 2 presses, all these variables would be:
    a1, a2, b1, b2, c1, c2 = firstVec[0], firstVec[1], secondVec[0], secondVec[1], resultVec[0], resultVec[1]
    # Now, the formula for x is (its really determinant devision):
    x = (b2*c1 - b1*c2) / (b2*a1 - b1*a2)
    #y = (a2*c1 - a1*c2) / (a2*b1 - a1*b2) worse, apparently
    y = (c1 - (a1 * x)) / b1 # Back substitution avoids precision problems somehow?
    if int(x) != x or int(y) != y:
        return [0, 0]
    else:
        return [int(x), int(y)]

def objOne(inputFile):
    lines = re.split("\n", inputFile.read())

    totalScore = 0

    for i in range(0, len(lines), 4):
        firstVec = (int(lines[i][12:14]), int(lines[i][18:20]))
        secondVec = (int(lines[i+1][12:14]), int(lines[i+1][18:20]))
        # Changed the + for obj 2
        resultNeeded = (int(re.split(",", lines[i+2])[0][9:]) + 10000000000000, int(re.split(",", lines[i+2])[1][3:]) + 10000000000000)
        
        # Reasonable approach
        # Now, stick them in a matrix
        res = sympy.Matrix([[firstVec[0], secondVec[0], resultNeeded[0]], [firstVec[1], secondVec[1], resultNeeded[1]]])
        res = res.rref()
        res = res[0]
        #print(res)

        buttonPresses = [res[0, 2] if type(res[0, 2]) == sympy.core.numbers.Integer else 0, res[1, 2] if type(res[1, 2]) == sympy.core.numbers.Integer else 0]

        buttonPresses = coefficientsManually(firstVec, secondVec, resultNeeded)
        
        totalScore += buttonPresses[0] * 3 + buttonPresses[1]
    print(totalScore)

if __name__ == "__main__":
    doctest.testmod()
    with open("advent_of_code_2024\\andrew\\Day13.txt", "r") as file:
        objOne(file)