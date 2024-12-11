import re

def parse_disk_map(disk_map_str):
    # Test Data has an odd number of values!
    matches = re.findall(r'(\d)(\d)|(\d)$', disk_map_str)
    files = []
    for file_length, free_length, single in matches:
        if single:
            files.append([int(single), 0])
        else:
            files.append([int(file_length), int(free_length)])
    return files

def create_initial_layout(files):
    layout = []
    file_id = 0
    for (file_length, free_length) in files:
        # Append file blocks
        if file_length > 0:
            layout.extend([file_id] * file_length)
            file_id += 1
        # Append free blocks
        if free_length > 0:
            layout.extend(['.'] * free_length)
    return layout

# Find a list of spots to put files. Returns an array of [length, start]
def find_free_spaces(layout):
    free_spans = []
    start = None
    for i, c in enumerate(layout):
        if c == '.':
            if start is None:
                start = i
        else:
            if start is not None:
                free_spans.append((start, i - start))
                start = None
    if start is not None:
        free_spans.append((len(layout) - start, start))
    return free_spans


def find_files(layout):
    """
    Identify the positions of each file.
    Return a dict: file_id -> (start_index, length)
    Assuming file_id may have multiple digits, parse accordingly.

    We'll parse each position to find continuous runs of identical non-'.' chars
    and assume they form a file of a single ID.
    """
    # Since file_id can be multiple digits, we need to correctly identify file blocks:
    # Each block is stored as a string like "0", "10", "11", ... (if we ever had multi-digit IDs).
    # However, from the original solution's approach, each block is just str(file_id),
    # so if we had file_id=12, each block would be "12" not single chars.
    # This means each block is a uniform string repeated multiple times.
    #
    # To handle multiple-digit IDs correctly, we need to group consecutive identical
    # non-'.' strings and treat them as one file.

    file_positions = {}
    visited_positions = set()

    for i, block in enumerate(layout):
        if block != '.' and i not in visited_positions:
            # Identify the file_id
            fid = block
            # Count how many consecutive blocks of the same file_id there are
            length = 1
            visited_positions.add(i)
            j = i + 1
            while j < len(layout) and layout[j] == fid:
                visited_positions.add(j)
                length += 1
                j += 1

            # Convert fid to int
            file_id = int(fid)
            file_positions[file_id] = (i, length)

    return file_positions


def move_files(layout):
    """
    Move whole files one by one, starting with the highest file_id,
    into the leftmost span of free space that can fit the entire file if possible.
    """
    # Find how many files we have and get their IDs
    file_positions = find_files(layout)
    if not file_positions:
        return layout  # No files to move

    max_id = max(file_positions.keys())

    for fid in range(max_id, -1, -1):
        # Refresh file positions because after moves, positions change
        file_positions = find_files(layout)
        if fid not in file_positions:
            continue
        start, length = file_positions[fid]

        # Find a suitable free space to the left of 'start' that can hold 'length' blocks
        # We only consider free spaces that end before 'start' (i.e. their end < start)
        # Actually, we need to consider any free space to the left of the file.
        free_spans = find_free_spaces(layout)

        # Filter free spans that completely end before the file starts
        # Actually, the problem states "If there is no span of free space to the left of a file..."
        # This means we must consider any free span that occurs *before* the file start,
        # i.e. span_start+span_length <= start
        suitable_spans = [(s, l) for (s, l) in free_spans if s + l <= start and l >= length]

        if not suitable_spans:
            # No suitable space found, don't move this file
            continue

        # Choose the leftmost suitable span
        # The "leftmost" span would be the one with the smallest start index s
        suitable_spans.sort(key=lambda x: x[0])
        chosen_start, chosen_length = suitable_spans[0]

        # Move the file to chosen_start
        # Remove the file blocks from current position
        file_blocks = layout[start:start + length]
        # Replace old location with '.'
        for i in range(start, start + length):
            layout[i] = '.'
        # Place file blocks at chosen_start
        for i in range(chosen_start, chosen_start + length):
            layout[i] = file_blocks[i - chosen_start]

    return layout

def compact_layout(layout):
    while True:
        # Find the leftmost '.' that is followed by a file block. (if there are no more blocks, we're done.
        dot_index = None
        for i, c in enumerate(layout):
            if c == '.':
                # Check if there's any file block to the right of this '.'
                if any(cc != '.' for cc in layout[i + 1:]):
                    dot_index = i
                    break

        if dot_index is None:
            # No '.' that is followed by a file block was found. We done.
            break

        # Find the rightmost file block (from the end)
        # Loop backwards. Had to look this one up. ):
        for j in range(len(layout) - 1, -1, -1):
            if layout[j] != '.':
                # Move this block to dot_index, and the '.' where the block used to be.
                layout[dot_index], layout[j] = layout[j], '.'
                break
    return layout


def compute_checksum(layout):
    # I have no idea how this would work as an actual checksum for files...But it's relatively simple math...
    checksum = 0
    for i, c in enumerate(layout):
        if c != '.':
            file_id = c
            checksum += i * file_id
    return checksum


# ---- TESTING WITH SAMPLE DATA ----
test_input = open('testinput.txt', 'r').read().rstrip()
test_pairs = parse_disk_map(test_input)
test_layout = create_initial_layout(test_pairs)
test_compacted = compact_layout(test_layout.copy())
test_checksum = compute_checksum(test_compacted)
print("Solution 1 Test:", test_checksum)

test_pairs2 = parse_disk_map(test_input)
test_layout2 = create_initial_layout(test_pairs2)
test_layout2 = move_files(test_layout2)
test_result_checksum2 = compute_checksum(test_layout2)
print("Solution 2 Test: ", test_result_checksum2)

# ---- REAL DATA ----
input = open('input.txt', 'r').read().rstrip()
pairs = parse_disk_map(input)
layout = create_initial_layout(pairs)
#compacted = compact_layout(layout.copy())
#checksum = compute_checksum(compacted)
#print("Solution 1:", checksum)

pairs2 = parse_disk_map(input)
layout2 = create_initial_layout(pairs2)
layout2 = move_files(layout2)
result_checksum2 = compute_checksum(layout2)
print("Solution 2 Test: ", result_checksum2)

