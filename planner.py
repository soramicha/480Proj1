import sys
import heapq

def main():
    # make sure we have the right number of arguments
    if len(sys.argv) != 3:
        print("Cannot Run Program")
        return 0
    
    # get coordinate of starting point
    expanded, col, row, layout, coord, goal_blocks = 0, 0, 0, [], [0, 0], []

    # read through the text file
    with open(sys.argv[2], 'r') as file:
        # get row and col values
        col = int(file.readline())
        row = int(file.readline())

        # read through the map layout line by line
        i = 0
        while True:
            x = file.readline()
            if x:
                # search if @ is found
                index = x.find("@")
                if index != -1:
                    # if so, store it into coord
                    coord = [i, index]
                # count the number of * and add it if any
                for j, val in enumerate(x):
                    if val == "*":
                        goal_blocks.append([i, j])
                layout.append(x[:len(x) - 1])
            else:
                break
            i += 1
        
    # created a visited arr
    visited = [[False for _ in range(col)] for _ in range(row)] 

    print(goal_blocks, "dirty blocks to clean total")
    
    # dfs
    if sys.argv[1] == "depth-first":
        print("Running depth first search...")
        dfs(coord[0], coord[1], visited, row, col, layout)

    else:
        print("Running uniform cost search...")
        path = ucs(coord, visited, row, col, layout, goal_blocks)
        """for index, p in enumerate(path):
            print("Path", index + 1)
            for i, j, d in p:
                print(d)
            print("V")"""
        for i in path:
            print(i)

    for i in range(row):
        for j in range(col):
            if visited[i][j]:
                expanded += 1

    print(row * col, "nodes generated")
    print(expanded, "nodes expanded")

def ucs(coord, visited, row, col, layout, goal_blocks):
    # assign cost and path
    queue = [(0, [[coord[0], coord[1], "Start"]])]
    goal_paths = []
    while queue:
        # first pop minimum cost and path from queue
        cost, path = heapq.heappop(queue)

        # get the last node from path
        x, y = path[-1][0], path[-1][1]

        # mark as visited
        visited[x][y] = True

        # if we cleaned up all blocks, return the cost and path
        if len(goal_blocks) == 0:
            return goal_paths
        
        # add to queue
        pattern = [(x + 1, y, x + 1 < row, "S"), (x - 1, y, x - 1 >= 0, "N"), (x, y + 1, y + 1 < col, "E"), (x, y - 1, y - 1 >= 0, "W")]
        for i, j, expression, direction in pattern:
            if expression and not visited[i][j] and layout[i][j] != "#":
                new = list(path)
                new.append([i, j, direction])
                if layout[i][j] == "*":
                    if [i, j] in goal_blocks:
                        goal_paths.append(new)
                        goal_blocks.remove([i, j])
                else:
                    heapq.heappush(queue, (cost + 2, new))

def dfs(x, y, visited, row, col, layout):
    # mark as true
    visited[x][y] = True

    if layout[x][y] == "*":
        print("V", x, y)

    # visited unvisited neighbors
    if x + 1 < row and not visited[x + 1][y] and layout[x + 1][y] != "#":
        print("S")
        dfs(x + 1, y, visited, row, col, layout)
    if x - 1 >= 0 and not visited[x - 1][y] and layout[x - 1][y] != "#":
        print("N")
        dfs(x - 1, y, visited, row, col, layout)
    if y + 1 < col and not visited[x][y + 1] and layout[x][y + 1] != "#":
        print("E")
        dfs(x, y + 1, visited, row, col, layout)
    if y - 1 >= 0 and not visited[x][y - 1] and layout[x][y - 1] != "#":
        print("W")
        dfs(x, y - 1, visited, row, col, layout)

if __name__ == "__main__":
    main()