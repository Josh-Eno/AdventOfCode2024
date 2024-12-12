from collections import Counter

"""
- If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
- If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
  The left half of the digits are engraved on the new left stone, and the right half of the digits are 
  engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become 
  stones 10 and 0.)
- If none of the other rules apply, the stone is replaced by a new stone; the old stone's number 
  multiplied by 2024 is engraved on the new stone.
"""
def transform(rock):
    rocks = []
    if rock == 0:
        rocks.append(1)
    elif len(str(rock)) % 2 == 0:
        rock = str(rock)
        new_rocks = [int(rock[:len(rock)//2]), int(rock[len(rock)//2:])]
        rocks.extend(new_rocks)
    else:
        new_rock = int(rock) * 2024
        rocks.append(new_rock)

    return rocks

def blink(map):
    output_map = Counter()
    for key in map:
        output = transform(key)
        for i in output:
            output_map[i] += 1 * map[key]

    return output_map


real_input = "9694820 93 54276 1304 314 664481 0 4"
test_input = "125 17"

input = list(map(int, real_input.split()))

summary = []
blinks = {}

count = 76
for i in range(1, count):
    if i == 1:
        # Turn our first input into a rock_map
        temp_map = Counter()
        for element in input:
            temp_map[element] = 1
        blinks[i] = blink(temp_map)
    else:
        blinks[i] = blink(blinks[i - 1])

print("Solution (" + str(count -1) + "): " + str(sum(blinks[list(blinks.keys())[-1]].values())))