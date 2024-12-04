import re

def objOne(file) -> None:
    sum = 0
    for line in file.readlines():
        matches = re.findall("mul\([0-9]{1,3},[0-9]{1,3}\)", line)
        print("Found " + str(len(matches)) + " matches")
        for match in matches:
            numbers = list(map(int, re.findall("\d{1,3}", match)))
            sum += numbers[0] * numbers[1]
    print(sum)

def objTwo(file) -> None:
    sum = 0
    enabled = True
    
    lines = file.read()

    # I'm just gonna pretend that this was my approach first try and I definitely didn't spend three hours on other solutions...
    matches = re.findall("(mul\(\d{1,3},\d{1,3}\))|(don't\(\))|(do\(\))", lines)

    enabled = True
    for match in matches:
        print(match)
        if match[0] != "": # Is it a mult? i.e. is it not a do/don't - 
            numbers = list(map(int, re.findall("\d{1,3}", match[0])))
            if enabled:
                print("Counted " + str(numbers[0]) + " * " + str(numbers[1]))
                sum += numbers[0] * numbers[1]
        elif match[1] != "":
            print("Disabled!")
            enabled = False
        elif match[2] != "":
            print("Enabled!")
            enabled = True

    print(sum)

if __name__ == "__main__":
    with open("advent_of_code_2024\\andrew\Day3.txt", "r") as file:
        objTwo(file)