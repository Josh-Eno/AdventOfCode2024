from collections import defaultdict
from typing import Dict, List, Set

class ThreeBitComputer:

    def __init__(self, registers: Dict[str, int], program: List[int], check: bool):
        self.registers = registers
        self.program = program
        self.inst_idx = 0
        self.output = []
        self.check = check

    def __str__(self):
        return f"Registers: {self.registers}\nProgram: {self.program}\nInstruction Index: {self.inst_idx}\nOutput: {self.output}"

    def check_output(self) -> bool:
        return True
        
    def run(self):
        while self.inst_idx < len(self.program) and self.check_output(): 
            instruction = self.program[self.inst_idx]
            literal_operand = self.program[self.inst_idx + 1]
            combo_operand = literal_operand

            match literal_operand:
                case 4:
                    combo_operand = self.registers['A']
                case 5:
                    combo_operand = self.registers['B']
                case 6:
                    combo_operand = self.registers['C']
                case 7:
                    raise ValueError("Invalid operand: 7")
                case _:
                    combo_operand = literal_operand

            match instruction:
                case 0:
                    self.registers['A'] = int(self.registers['A'] / (2 ** combo_operand))
                    self.inst_idx += 2
                case 1:
                    self.registers['B'] = self.registers['B'] ^ literal_operand
                    self.inst_idx += 2
                case 2:
                    self.registers['B'] = combo_operand % 8
                    self.inst_idx += 2
                case 3:
                    self.inst_idx = self.inst_idx + 2 if self.registers['A'] == 0 else literal_operand
                case 4:
                    self.registers['B'] = self.registers['B'] ^ self.registers['C']
                    self.inst_idx += 2
                case 5:
                    self.output.append(combo_operand % 8)
                    self.inst_idx += 2
                case 6:
                    self.registers['B'] = int(self.registers['A'] / (2 ** combo_operand))
                    self.inst_idx += 2
                case 7:
                    self.registers['C'] = int(self.registers['A'] / (2 ** combo_operand))
                    self.inst_idx += 2
                case _:
                    print(f"Unknown instruction: {instruction}")
                    break
            # print(self)
            

    def get_output(self):
        return ",".join(map(str, self.output))
'''
Register A: 66171486
Register B: 0
Register C: 0

Program: 2,4,1,6,7,5,4,6,1,4,5,5,0,3,3,0`
'''

prod_comp = ThreeBitComputer({'A': 66171486, 'B': 0, 'C': 0}, [2,4,1,6,7,5,4,6,1,4,5,5,0,3,3,0], False)
prod_comp.run()
print(f"Part 1 output: {prod_comp.get_output()}")

# Search from back to front
targets = [0, 3, 3, 0, 5, 5, 4, 1, 6, 4, 5, 7, 6, 1, 4, 2] 
valid_set = {0}
for idx, target in enumerate(targets):
    next_valid: Set[int] = set() 
    for valid_a in valid_set:
        valid_states = defaultdict(list)
        min_a = valid_a << 3
        max_a = min_a + 8
        for a in range(min_a, max_a):
            last_comp = ThreeBitComputer({'A': a, 'B': 0, 'C': 0}, [2, 4, 1, 6, 7, 5, 4, 6, 1, 4, 5, 5, 0, 3], False)
            last_comp.run()
            if last_comp.get_output() == str(target):
                next_valid.add(a)
            
    print(f"For target {target} at idx {idx}, next_valid = {next_valid}")
    valid_set = next_valid


valid_list = list(valid_set)
valid_list.sort()
print(f"Min valid input: {valid_list[0]}")

last_comp = ThreeBitComputer({'A': 90938893795561, 'B': 0, 'C': 0}, [2, 4, 1, 6, 7, 5, 4, 6, 1, 4, 5, 5, 0, 3, 3, 0], False)
last_comp.run()
output = last_comp.get_output()
print(output)
assert output == ",".join(map(str, last_comp.program))

'''
# This was so bad....
found = False
idx = 0
while not found:
    test_comp = ThreeBitComputer({'A': idx, 'B': 0, 'C': 0}, [2, 4, 1, 6, 7, 5, 4, 6, 1, 4, 5, 5, 0, 3, 3, 0], True)
    test_comp.run()
    output = test_comp.get_output()
    if len(output) == 16 and test_comp.check_output():
        found = True
        print(f"Found it: {idx}")
        break

    idx += 1

    if idx % 1000000 == 0:
        print(f"Trying {idx}")
'''