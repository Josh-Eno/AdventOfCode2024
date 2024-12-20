import os
import networkx

def objOne(fileContent: str):
    coords = fileContent.split("\n")
    gridSize = 71
    coordSpace = [['.' for _ in range(gridSize)] for _ in range(gridSize)]
    index = 0
    for coord in coords:
        if index < 3011:
            coordSpace[int(coord.split(",")[1])][int(coord.split(',')[0])] = "#"# coordSpace[y][x]
            index += 1
    
    for line in coordSpace:
        for char in line:
            print(char, end="")
        print()

    graph = networkx.DiGraph()
    for line in range(len(coordSpace)):
        for char in range(len(coordSpace[line])):
            if coordSpace[line][char] == ".":
                graph.add_node((line, char)) # Nodes are stored line, col
    
    for node in graph.nodes():
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for dir in directions:
            if graph.has_node((node[0] + dir[0], node[1] + dir[1])):
                graph.add_edge(node, (node[0] + dir[0], node[1] + dir[1]))
    
    #print(len(graph.edges()))
    print(len(networkx.shortest_path(graph, (0, 0), (70, 70))) - 1)


with open(os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), "Day18.txt"), "r") as file:
    objOne(file.read())
    # To do objective two, just run objective one with different end indices to get the actual number when it fails
    # Then check the line number of that coord