from typing import Dict, List, Set

class Component:
    def __init__(self, r, c, garden: List[List[str]]):
        self.garden = garden
        self.plots: Set[tuple] = {(r, c)}
        self.char: str = garden[r][c]
        self.grow()
        self.area = len(self.plots)
        self.perimeter_plots: Set[tuple] = set()
        self.perimeter = self.calc_perimeter()
        self.sides = self.calc_sides_edges()
        self.corners = self.calc_corners()
        self.cost_1 = self.area * self.perimeter
        self.cost_2 = self.area * self.sides
        self.cost_3 = self.area * self.corners
        if self.sides != self.corners:
            print(f"origin: {r}, {c}, char: {self.char}, area: {self.area}, perimeter: {self.perimeter}, sides: {self.sides}, corners: {self.corners}, cost 1: {self.cost_1}, cost 2: {self.cost_2}, cost 3: {self.cost_3}")

    def grow(self):
        new_frontier: Set[tuple] = self.plots
        while new_frontier:
            frontier = new_frontier
            new_frontier = set()
            for plot in frontier:
                if plot[0] > 0 and self.garden[plot[0] - 1][plot[1]] == self.char and (plot[0] - 1, plot[1]) not in self.plots:
                    new_frontier.add((plot[0] - 1, plot[1]))
                if plot[0] < len(self.garden) - 1 and self.garden[plot[0] + 1][plot[1]] == self.char and (plot[0] + 1, plot[1]) not in self.plots:
                    new_frontier.add((plot[0] + 1, plot[1]))
                if plot[1] > 0 and self.garden[plot[0]][plot[1] - 1] == self.char and (plot[0], plot[1] - 1) not in self.plots:
                    new_frontier.add((plot[0], plot[1] - 1))
                if plot[1] < len(self.garden[0]) - 1 and self.garden[plot[0]][plot[1] + 1] == self.char and (plot[0], plot[1] + 1) not in self.plots:
                    new_frontier.add((plot[0], plot[1] + 1))
            self.plots.update(new_frontier)

    def calc_perimeter(self):
        perimeter = 0
        for plot in self.plots:
            if (plot[0] - 1,  plot[1]) not in self.plots:
                perimeter += 1
            if (plot[0] + 1,  plot[1]) not in self.plots:
                perimeter += 1
            if (plot[0],  plot[1] - 1) not in self.plots:
                perimeter += 1
            if (plot[0], plot[1] + 1) not in self.plots:
                perimeter += 1
            if perimeter > 0:
                self.perimeter_plots.add(plot)

        return perimeter

    def calc_sides_edges(self):
        shared_sides = 0
        considered: Set[tuple] = set()
        for plot in self.perimeter_plots:
            neighbor_plots = self.get_neighbor_candidates(plot)
            considered.add(plot)
            for neighbor in neighbor_plots:
                if neighbor in considered or neighbor not in self.perimeter_plots:
                    continue
                if self.open_right(plot) and self.open_right(neighbor):
                    shared_sides += 1
                if self.open_left(plot) and self.open_left(neighbor):
                    shared_sides += 1
                if self.open_down(plot) and self.open_down(neighbor):
                    shared_sides += 1
                if self.open_up(plot) and self.open_up(neighbor):
                    shared_sides += 1
                
                # if shared_sides > 0:
                #     print(f"shared side between ({plot[0]}, {plot[1]}) and ({neighbor[0]}, {neighbor[1]})")
        
        return self.perimeter - shared_sides

    def calc_corners(self):
        corners = 0
        for plot in self.perimeter_plots:
            # Check outer corners
            if self.open_up(plot):
                # Outer corner |—
                if self.open_left(plot):
                    corners += 1
                # Outer corner —|
                if self.open_right(plot):
                    corners += 1
                # Inner orner _|, from below
                if (plot[0] - 1, plot[1] + 1) in self.perimeter_plots and (plot[0], plot[1] + 1) in self.plots:
                    corners += 1
                # Inner corner |_, from below
                if (plot[0] - 1, plot[1] - 1) in self.perimeter_plots and (plot[0], plot[1] - 1) in self.plots:
                    corners += 1
            if self.open_down(plot):
                # Outer corner |_
                if self.open_left(plot):
                    corners += 1
                # Outer corner _|
                if self.open_right(plot):
                    corners += 1
                # Inner corner —|
                if (plot[0] + 1, plot[1] + 1) in self.perimeter_plots and (plot[0], plot[1] + 1) in self.plots:
                    corners += 1
                # Inner corner |—
                if (plot[0] + 1, plot[1] - 1) in self.perimeter_plots and (plot[0], plot[1] - 1) in self.plots:
                    corners += 1
         
        return corners
    
    def open_right(self, plot: tuple) -> bool:
        return plot[1] == len(self.garden[0]) - 1 or self.garden[plot[0]][plot[1]] != self.garden[plot[0]][plot[1] + 1]
    
    def open_left(self, plot: tuple) -> bool:
        return plot[1] == 0 or self.garden[plot[0]][plot[1]] != self.garden[plot[0]][plot[1] - 1]

    def open_up(self, plot: tuple) -> bool:
        return plot[0] == 0 or self.garden[plot[0]][plot[1]] != self.garden[plot[0] - 1][plot[1]]
        
    def open_down(self, plot: tuple) -> bool:
        return plot[0] == len(self.garden) - 1 or self.garden[plot[0]][plot[1]] != self.garden[plot[0] + 1][plot[1]]

    def get_neighbor_candidates(self, plot: tuple):
        neighbors = []
        if plot[0] > 0:
            neighbors.append((plot[0] - 1, plot[1]))
        if plot[0] < len(self.garden) - 1:
            neighbors.append((plot[0] + 1, plot[1]))
        if plot[1] > 0:
            neighbors.append((plot[0], plot[1] - 1))
        if plot[1] < len(self.garden[0]) - 1:
            neighbors.append((plot[0], plot[1] + 1))
        return neighbors

input = [
    "OOOOO",
    "OXOXO",
    "OOOOO",
    "OXOXO",
    "OOOOO"
]
input = [
    "RRRRIICCFF",
    "RRRRIICCCF",
    "VVRRRCCFFF",
    "VVRCCCJFFF",
    "VVVVCJJCFE",
    "VVIVCCJJEE",
    "VVIIICJJEE",
    "MIIIIIJJEE",
    "MIIISIJEEE",
    "MMMISSJEEE"
]
input = [
    "EEEEE",
    "EXXXX",
    "EEEEE",
    "EXXXX",
    "EEEEE"
]
input = [
    "AAAAAA",
    "AAABBA",
    "AAABBA",
    "ABBAAA",
    "ABBAAA",
    "AAAAAA"
]
input = open("./advent_of_code_2024/josh/day12/input.txt").read().splitlines()

seen_plots: Set[tuple] = set()
components = []
for r in range(len(input)):
    for c in range(len(input[0])):
        if (r, c) not in seen_plots:
            comp = Component(r, c, input)
            seen_plots.update(comp.plots)
            components.append(comp)

p1_cost = sum(map(lambda comp: comp.cost_1, components))
p2_cost = sum(map(lambda comp: comp.cost_2, components))
p3_cost = sum(map(lambda comp: comp.cost_3, components))

print(f"cost 1: {p1_cost}")
print(f"cost 2: {p2_cost}")  
print(f"cost 3: {p3_cost}")  
