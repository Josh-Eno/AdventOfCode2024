input = open("./advent_of_code_2024/josh/day9/input.txt").read().strip()
# input = "2333133121414131402"

gaps = []
files = []
compacted = []
for idx, c in enumerate(input):
    if idx % 2 == 0:
        files.append(c)
        compacted.extend([int(idx / 2)] * int(c))
    else:
        gaps.append(c)
        compacted.extend(['.'] * int(c))

insert_idx = 0
move_idx = len(compacted) - 1
while compacted[insert_idx] != '.':
    insert_idx += 1

steps = 0
while move_idx > insert_idx:
    move_val = compacted[move_idx]
    compacted[insert_idx] = move_val
    compacted[move_idx] = '.'
    move_idx -= 1
    while compacted[insert_idx] != '.' and insert_idx < move_idx:
        insert_idx += 1
    steps += 1
    
checksum = 0
for idx, val in enumerate(compacted):
    if val == '.':
        break
    checksum += val * idx

print(f"checksum: {checksum}")