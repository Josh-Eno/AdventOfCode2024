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

def move_element(room: List[str], from_pos: Tuple[int, int], direction: str) -> Tuple[int, int]:
    to_pos = map_pos(from_pos, direction)
    this_element = get_element(room, from_pos)
    dest_element = get_element(room, to_pos)
    if dest_element == "#":
        return from_pos
    elif dest_element == "O":
        moved_pos = move_element(room, to_pos, direction)
        if moved_pos != to_pos :
            room[to_pos[0]][to_pos[1]] = this_element
            room[from_pos[0]][from_pos[1]] = "."
            return to_pos
        return from_pos
    else:
        room[to_pos[0]][to_pos[1]] = this_element
        room[from_pos[0]][from_pos[1]] = "."
        return to_pos
        
def read_the_room(input: List[str]):
    room: List[str] = []
    instructions: str = ""
    robot = (0, 0)
    for row, line in enumerate(input):
        if line.startswith("#"):
            room.append(list(line))
            robot_idx = line.find("@")
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
        if room[r][c] == "O":
            total += 100 * r + c

print(f"total: {total}")