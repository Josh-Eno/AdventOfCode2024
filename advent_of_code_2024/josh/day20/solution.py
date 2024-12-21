from collections import defaultdict

class Track:
    def __init__(self, track):
        self.track = track
        self.find_ends()
        self.find_route()
    
    def __str__(self):
        output = f"start: {self.start}, end: {self.end}, route: {self.route}"

    def find_ends(self):
        for r in range(len(self.track)):
            for c in range(len(self.track[0])):
                if self.track[r][c] == "S":
                    self.start = (r, c)
                elif self.track[r][c] == "E":
                    self.end = (r, c)
            
        print(f"start: {self.start}, end: {self.end}")
    
    @staticmethod
    def manhattan_dist(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_route(self):
        self.route = [self.start]

        while self.route[-1] != self.end:
            prev_node = self.route[-1]
            up = (self.track[prev_node[0]-1][prev_node[1]], (prev_node[0] - 1, prev_node[1]))
            down = (self.track[prev_node[0]+1][prev_node[1]], (prev_node[0] + 1, prev_node[1]))
            right = (self.track[prev_node[0]][prev_node[1]+1], (prev_node[0], prev_node[1] + 1))
            left = (self.track[prev_node[0]][prev_node[1]-1], (prev_node[0], prev_node[1] - 1))

            next_node = up[1] if up[1] not in self.route and (up[1] == self.end or up[0] == ".") else \
                down[1] if down[1] not in self.route and (down[1] == self.end or down[0] == ".") else \
                left[1] if left[1] not in self.route and (left[1] == self.end or left[0] == ".") else \
                right[1] if right[1] not in self.route and (right[1] == self.end or right[0] == ".") else None
                
            self.route.append(next_node)
        
        print(f"Total distance: {len(self.route)}")

    def get_item_index(self, item):
        try:
            return self.route.index(item)
        except ValueError:
            return -1

    def count_cheats(self, min=0):
        self.cheats = defaultdict(int)
        for s_idx, node in enumerate(self.route):
            for n_idx in range(s_idx + 2 + min, len(self.route)):
                n_node = self.route[n_idx]
                dist = self.manhattan_dist(node, n_node)
                skip_dist = (n_idx - s_idx - dist) if dist <= 20 else 0
                
                if skip_dist >= min:
                    self.cheats[skip_dist] += 1


input_file = open("./advent_of_code_2024/josh/day20/input.txt").read().splitlines()
input_test = [
    "###############",
    "#...#...#.....#",
    "#.#.#.#.#.###.#",
    "#S#...#.#.#...#",
    "#######.#.#.###",
    "#######.#.#...#",
    "#######.#.###.#",
    "###..E#...#...#",
    "###.#######.###",
    "#...###...#...#",
    "#.#####.#.###.#",
    "#.#...#.#.#...#",
    "#.#.#.#.#.#.###",
    "#...#...#...###",
    "###############"
]

track = Track(input_file)
track.count_cheats(100)

keys = list(track.cheats.keys())
keys.sort()
total_cheats = 0
for k in keys:
    total_cheats += track.cheats[k]
    print(f"{k}: {track.cheats[k]}")

print(f"Total cheats that save at least 100: {total_cheats}")
