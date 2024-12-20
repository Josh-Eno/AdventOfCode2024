import os
import math

instructionPointer = 0
registerA = 0
registerB = 0
registerC = 0
output = []

def executeOperand(inst: int, operand: int, instructionPointer, registerA, registerB, registerC, output) -> tuple[int, int, int, int, list]: # Bool is if you should increment the instruction pointer
    # Tuple is instructionPointer, regA, regB, regC, output
    litOperand = operand
    comboOperand = operand
    if comboOperand == 4:
        comboOperand = registerA
    elif comboOperand == 5:
        comboOperand = registerB
    elif comboOperand == 6:
        comboOperand = registerC
    if inst == 0: # Division operator, goes to the A register
        return (instructionPointer + 2, math.floor(registerA / (math.pow(2, comboOperand))), registerB, registerC, output)
    elif inst == 1: # Bitwise or operator, goes to the B register
        tempA = str(bin(litOperand))
        tempB = str(bin(registerB))
        result = ""
        while len(tempA) < len(tempB):
            tempA = "0" + tempA
        while len(tempB) < len(tempA):
            tempB = "0" + tempB
        for cha in range(len(tempA)):
            result += '1' if tempA[cha] != tempB[cha] else '0' # XOR is that simple
        return (instructionPointer + 2, registerA, int(result[2:], 2), registerC, output)
    elif inst == 2: # Combo % 8, goes to the B register
        return (instructionPointer + 2, registerA, comboOperand % 8, registerC, output)
    elif inst == 3: # Jump operator
        if registerA != 0:
            return (litOperand, registerA, registerB, registerC, output)
        else:
            return (instructionPointer + 2, registerA, registerB, registerC, output)
    elif inst == 4: # Bitwise OR on c and b, result goes to b
        tempA = f"{registerC:b}"
        tempB = f"{registerB:b}"
        result = ""
        # Correct their lengths so they are equal
        while len(tempA) < len(tempB):
            tempA = "0" + tempA
        while len(tempB) < len(tempA):
            tempB = "0" + tempB
        for cha in range(len(tempA)):
            result += '1' if tempA[cha] != tempB[cha] else '0' # XOR is that simple
        registerB = int(result, 2)
        return (instructionPointer + 2, registerA, int(result, 2), registerC, output)
    elif inst == 5: # Combo % 8, puts value in the output
        res = output
        res.append(comboOperand % 8)
        return (instructionPointer + 2, registerA, registerB, registerC, res)
    elif inst == 6: # bdivide, same as 0 just in the B register
        return (instructionPointer + 2, registerA, math.floor(registerA / (math.pow(2, comboOperand))), registerC, output)
    elif inst == 7: # cdivide, same as 0 just in the C register
        return (instructionPointer + 2, registerA, registerB, math.floor(registerA / (math.pow(2, comboOperand))), output)

def objOne(fileContent: str):
    global instructionPointer
    global registerA
    global registerB
    global registerC
    global output
    lines = fileContent.strip().split("\n")
    registers = [int(x.split(": ")[1]) for x in lines[0:3]]
    registerA = registers[0]
    registerB = registers[1]
    registerC = registers[2]
    # Now, run the program
    program = [int(x) for x in lines[len(lines)-1].split(": ")[1].split(",")]
    halt = False
    while not halt:
        print(instructionPointer)
        if 0 <= instructionPointer < len(program)-1: # Because the index after the instruction pointer will be the operand
            result =  executeOperand(program[instructionPointer], program[instructionPointer+1], instructionPointer, registerA, registerB, registerC, output)
            instructionPointer = result[0]
            registerA = result[1]
            registerB = result[2]
            registerC = result[3]
            output = result[4]
        else: # Got to the end, halt
            halt = True
    print(str(output)[1:-1].replace(" ", ""))

def objTwo(fileContent: str):
    lines = fileContent.strip().split("\n")

with open(os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), "Day17.txt"), "r") as file:
    objOne(file.read())