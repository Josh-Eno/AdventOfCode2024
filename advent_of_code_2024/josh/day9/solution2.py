import json
from typing import List

class File:
    def __init__(self, number, length):
        self.number = number
        self.length = length
    
    def to_str(self):
        return f"File: {self.number} {self.length}"

input = open("./advent_of_code_2024/josh/day9/input.txt").read().strip()
# input = "2333133121414131402"

# files are tuples of (idx, length). If it's a gap, the idx is -1
files: List[File] = []
for idx, c in enumerate(input):
    if idx % 2 == 0:
        files.append(File(int(idx / 2), int(c)))
    else:
        files.append(File(-1, int(c)))

f_idx = len(files) - 1
while f_idx > 0:
    file = files[f_idx]
    file_size = file.length
    offset = -1
    move_idx = 0
    if file.number == -1:
        f_idx -= 1
        continue

    while move_idx < f_idx:
        if files[move_idx].number != -1:
            move_idx += 1
            continue

        if files[move_idx].length >= file_size:
            gap = files[move_idx]
            remaining = gap.length - file_size
            files[f_idx] = File(-1, file_size)
            if remaining == 0:
                files[move_idx] = file
                offset = -1 
            else:
                gap.length = remaining
                files.insert(move_idx, file)
                offset = 0

            # Skip out on the rest of the files
            move_idx = f_idx
        else:
            move_idx += 1

    f_idx += offset

checksum = 0
idx = 0
for file in files:
    if file.number == -1:
        idx += file.length
    else:
        for i in range(file.length):
            checksum += idx * file.number
            idx += 1

print(f"checksum: {checksum}")