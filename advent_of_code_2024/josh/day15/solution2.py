from typing import List, Tuple

input1 = [
    "########",
    "#..O.O.#",
    "##@.O..#",
    "#...O..#",
    "#.#.O..#",
    "#...O..#",
    "#......#",
    "########",
    "",
    "<^^>>>vv<v>>v<<",
]

input2 = [
    "##########",
    "#..O..O.O#",
    "#......O.#",
    "#.OO..O.O#",
    "#..O@..O.#",
    "#O#..O...#",
    "#O..O..O.#",
    "#.OO.O.OO#",
    "#....O...#",
    "##########",
    "",
    "<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"
]

input_file = open("./advent_of_code_2024/josh/day15/input.txt").read().splitlines()

move_map = {
    "<": (0, -1),
    "^": (-1, 0),
    "v": (1, 0),
    ">": (0, 1),
}

def to_str(room: List[List[str]]):
    return "\n".join(["".join(row) for row in room])

def map_pos(pos: Tuple[int, int], direction: str) -> Tuple[int, int]:
    return (pos[0] + move_map[direction][0], pos[1] + move_map[direction][1])

def get_element(room: List[List[str]], pos: Tuple[int, int]) -> str:
    return room[pos[0]][pos[1]]

def can_move(room: List[List[str]], pos: Tuple[int, int], direction: str) -> bool:
    to_pos = map_pos(pos, direction)
    to_element = get_element(room, to_pos)
    if to_element == "#":
        return False
    if to_element == ".":
        return True
    elif direction == "<" or direction == ">":
        return can_move(room, to_pos, direction)
    elif to_element == "[":
        return can_move(room, to_pos, direction) and can_move(room, (to_pos[0], to_pos[1] + 1), direction)
    elif to_element == "]":
        return can_move(room, to_pos, direction) and can_move(room, (to_pos[0], to_pos[1] - 1), direction)
    else:
        print(f"Oops! can_move invalid char at pos: {pos}, dir: {direction}")
        print(to_str(room))
        return False
    
# Only call this after we determine we _can_ move. Moves one position only.
def move_recursively(room: List[str], from_pos: Tuple[int, int], direction: str):
    to_pos = map_pos(from_pos, direction)
    this_element = get_element(room, from_pos)
    next_element = get_element(room, to_pos)
    if next_element == "#":
        return
    if next_element != ".":
        if direction == "<" or direction == ">":
            move_recursively(room, to_pos, direction)
        else:
            to_element = get_element(room, to_pos)
            if (this_element == "[" or this_element == "@") and to_element == "]":
                move_recursively(room, to_pos, direction)
                move_recursively(room, (to_pos[0], to_pos[1] - 1), direction)
            elif (this_element == "]" or this_element == "@") and to_element == "[":
                move_recursively(room, to_pos, direction)
                move_recursively(room, (to_pos[0], to_pos[1] + 1), direction)
            else:
                move_recursively(room, to_pos, direction)

    room[to_pos[0]][to_pos[1]] = this_element
    room[from_pos[0]][from_pos[1]] = "."

def move_element(room: List[str], from_pos: Tuple[int, int], direction: str) -> Tuple[int, int]:
    to_pos = map_pos(from_pos, direction)
    should_move = can_move(room, from_pos, direction)
    if should_move:
        move_recursively(room, from_pos, direction)
        return to_pos
    return from_pos
        
def expand(line: str) -> List[str]:
    return list(line.replace(".", "..").replace("@", "@.").replace("#", "##").replace("O", "[]"))

def read_the_room(input: List[str]):
    room: List[str] = []
    instructions: str = ""
    robot = (0, 0)
    for row, line in enumerate(input):
        if line.startswith("#"):
            expanded = expand(line)
            room.append(expanded)
            robot_idx = "".join(expanded).find("@")
            if robot_idx > 0:
                robot = (row, robot_idx)
        elif line == "":
            pass
        else:
            instructions += line.strip()
    return (room, instructions, robot)

room, instructions, robot = read_the_room(input_file)

for idx, instruction in enumerate(instructions):
    robot = move_element(room, robot, instruction)

total = 0
for r in range(len(room)):
    for c in range(len(room[r])):
        if room[r][c] == "[":
            total += 100 * r + c

print(f"total: {total}")