import sys
import heapq
import itertools

def main():
    # make sure we have the right number of arguments
    if len(sys.argv) != 3:
        print("Cannot Run Program")
        return 0
    
    # define variables
    nodes_generated, expanded, col, row, layout, coord, goal_blocks, blocks = [1], 0, 0, 0, [], [0, 0], [], 0

    # read through the text file
    with open(sys.argv[2], 'r') as file:
        # get row and col values
        col = int(file.readline())
        row = int(file.readline())

        # read through the map layout line by line
        i = 0 # variable to keep track of the row
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
                    # count any obstacles as well
                    if val == "#":
                        blocks += 1
                layout.append(x[:len(x) - 1])
            else:
                break
            i += 1 # increment row i by 1
        
    print(goal_blocks, "dirty blocks to clean total")

    # get the number of tiles we can actually travel and access
    good_tiles = row * col - blocks
    
    # dfs
    if sys.argv[1] == "depth-first":
        # inform user what algorithm we're running
        print("Running depth first search...")

        # create a visited 2D array
        visited = [[False for _ in range(col)] for _ in range(row)]

        # run dfs
        path = dfs(coord, visited, row, col, layout, [], good_tiles)


        new_visit = [[False for _ in range(col)] for _ in range(row)]
        c = 0
        # extract the path we need (exclude the path where the robot goes back to where it started)
        for index, p in enumerate(path):
            if not new_visit[p[0]][p[1]]:
                c += 1
            if c == good_tiles:
                c = index
                break
            new_visit[p[0]][p[1]] = True

        # keep track of which goals we visited
        visited_goals = []

        # calculate the number of nodes generated while traveling in this path
        prev = path[0]
        for p in path[1:c + 1]:
            # calculate direction
            if prev[0] - p[0] == -1:
                print("S")
            elif prev[0] - p[0] == 1:
                print("N")
            elif prev[1] - p[1] == -1:
                print("E")
            else:
                print("W")

            # assign new prev to current p
            prev = p

            # if it's a dirty tile and the goal isn't included in visited_goals
            if layout[p[0]][p[1]] == "*" and [p[0], p[1]] not in visited_goals:
                # add to visited goals
                visited_goals.append([p[0], p[1]])
                # print V for vaccuum
                print("V")

            # assign x and y
            x, y = p[0], p[1]
            pattern = [x + 1 < row, x - 1 >= 0, y + 1 < col, y - 1 >= 0]

            # go through the pattern
            nodes_generated[0] += sum(1 if expression else 0 for expression in pattern)

        # get the number of visited nodes using visited
        for i in range(row):
            for j in range(col):
                if visited[i][j]:
                    expanded += 1
    else:
        # inform user what algorithm we're running
        print("Running uniform cost search...")
        
        # get all different ways robot can move to approach which goal in order
        permutations = itertools.permutations(goal_blocks)

        # get best result
        best_res = []

        for permutation in permutations:
            # set the starting coordinate for every permutation
            start = coord

            # keep track of the overall path per permutation
            path = []

            # assign permutation into an ordered list
            order_of_goals = list(permutation)

            # begin following the permutation order
            for index, goal in enumerate(permutation):
                # if the current goal isn't in the order_of_goals,
                if goal not in order_of_goals:
                    # then simply skip it
                    continue

                # uniform-cost search
                new_path = ucs(start, row, col, layout, order_of_goals, goal)

                if index == 0:
                    # get the path that will reach that specific goal from start
                    path += new_path
                else:
                    path += new_path[1:]

                # new start at goal and we will keep looping until the last goal
                start = goal

            # if best_res is empty, assign to current path
            if best_res == []:
                best_res.append(path)
            # otherwise, compare the lengths and reassign best_res if needed
            elif len(best_res[0]) > len(path):
                best_res[0] = path

        # keep track of number of visited nodes
        expanded = 0

        # keep track of which goals we visited
        visited_goals = []
        
        # print out final path for a permutation order
        # ALSO calculate the number of nodes generated while traveling in this path        
        for p in best_res[0]:
            # increment visited nodes by 1
            expanded += 1

            # print out the direction
            print(p[2])

            # if it's a dirty cell, print V
            if len(p) == 4 and [p[0], p[1]] not in visited_goals:
                print("V")

                # add to visited goals
                visited_goals.append([p[0], p[1]])

            # assign x and y
            x, y = p[0], p[1]
            pattern = [x + 1 < row, x - 1 >= 0, y + 1 < col, y - 1 >= 0]

            # go through the pattern
            nodes_generated[0] += sum(1 if expression else 0 for expression in pattern)
        
    # total number of nodes in the queue
    print(nodes_generated[0], "nodes generated")
    # total number of nodes visited
    print(expanded, "nodes expanded")

def ucs(coord, row, col, layout, order_of_goals, goal):
    # start off the queue and assign the current cost and path
    queue = [(0, [[coord[0], coord[1], "Start"]])]
    
    # loop until queue is empty
    while queue:
        # first pop minimum cost and path from queue
        cost, path = heapq.heappop(queue)

        # get the last node from path
        x, y = path[-1][0], path[-1][1]

        # generate a pattern array for all directions
        pattern = [(x + 1, y, x + 1 < row, "S"), (x - 1, y, x - 1 >= 0, "N"), (x, y + 1, y + 1 < col, "E"), (x, y - 1, y - 1 >= 0, "W")]

        # add to queue
        for i, j, expression, direction in pattern:
            # if it's not a blocked tile and there exists a path in this direction
            if expression and layout[i][j] != "#":
                # create a new array with the current path
                new = list(path)
                
                # if we find the goal
                if layout[i][j] == "*" and [i, j] == goal:
                    # add to the new path
                    new.append([i, j, direction, 'V'])

                    # remove all goals we've come across during our optimal path
                    for node in new:
                        if [node[0], node[1]] in order_of_goals:
                            order_of_goals.remove([node[0], node[1]])

                    # return the overall goal path
                    return new
                # if it's another goal, label the cost as 1
                elif layout[i][j] == "*":
                    new.append([i, j, direction, 'V'])
                    heapq.heappush(queue, (cost + 1, new))
                # otherwise label the cost as 2
                else:
                    new.append([i, j, direction])
                    heapq.heappush(queue, (cost + 2, new))

def dfs(coord, visited, row, col, layout, path, good_tiles):
    # extract x and y coordinates
    x, y = coord[0], coord[1]

    # mark as true
    visited[x][y] = True

    # add coord to path
    path.append(coord)

    # find how many nodes we've visited
    v = 0
    for i in range(row):
        for j in range(col):
            if visited[i][j]:
                v += 1
    
    if v == good_tiles:
        return path

    # visited all unvisited neighbors in all 4 directions
    if x + 1 < row and not visited[x + 1][y] and layout[x + 1][y] != "#":
        dfs([x + 1, y], visited, row, col, layout, path, good_tiles)
        # backtracking
        path.append(coord)
    if x - 1 >= 0 and not visited[x - 1][y] and layout[x - 1][y] != "#":
        dfs([x - 1, y], visited, row, col, layout, path, good_tiles)
        # backtracking
        path.append(coord)
    if y + 1 < col and not visited[x][y + 1] and layout[x][y + 1] != "#":
        dfs([x, y + 1], visited, row, col, layout, path, good_tiles)
        # backtracking
        path.append(coord)
    if y - 1 >= 0 and not visited[x][y - 1] and layout[x][y - 1] != "#":
        dfs([x, y - 1], visited, row, col, layout, path, good_tiles)
        # backtracking
        path.append(coord)

    return path

if __name__ == "__main__":
    main()