class Equation:
    def __init__(self, line):
        self.target = int(line.split(":")[0])
        self.elems = list(map(int, line.split(":")[1].strip().split(" "))) 
        
    # Returns target if valid, 0 otherwise
    def is_valid(self) -> int:
        candidates = [self.elems.copy()]
        next_candidates = []
        while len(candidates[0]) > 1:
            for candidate in candidates:
                next_candidates.append([candidate[0] + candidate[1]] + candidate[2:])
                next_candidates.append([candidate[0] * candidate[1]] + candidate[2:])
                next_candidates.append([int(str(candidate[0]) + str(candidate[1]))] + candidate[2:])
            candidates = next_candidates
            next_candidates = []

        finals = list(map(lambda x: x[0], candidates))
        if self.target in finals:
            return self.target
        return 0

input = [
    "190: 10 19",
    "3267: 81 40 27",
    "83: 17 5",
    "156: 15 6",
    "7290: 6 8 6 15",
    "161011: 16 10 13",
    "192: 17 8 14",
    "21037: 9 7 18 13",
    "292: 11 6 16 20"
]
input = open("./advent_of_code_2024/josh/day7/input.txt").read().strip().split("\n")

equations = list(map(Equation, input))

print(len(equations))
print(sum(map(lambda x: x.is_valid(), equations)))