#!python3
import collections

def read_map(file):
    cave_map = []
    with open(file) as input_file:
        for line in input_file:
            cave_map.append(list(line.strip('\n')))
    return cave_map.copy()

def find_portals(cave_map):
    portals_dict = {}
    nbr_of_rows = len(cave_map)
    nbr_of_cols = len(cave_map[0])
    for r in range(1,nbr_of_rows-1):
        for c in range(1, nbr_of_cols-1):
            if cave_map[r][c].isupper():
                if cave_map[r+1][c] == '.':
                    name = cave_map[r][c] + cave_map[r-1][c]
                    name = ''.join(sorted(name))
                elif cave_map[r][c+1] == '.':
                    name = cave_map[r][c] + cave_map[r][c-1]
                    name = ''.join(sorted(name))
                elif cave_map[r-1][c] == '.':
                    name = cave_map[r][c] + cave_map[r+1][c]
                    name = ''.join(sorted(name))
                elif cave_map[r][c-1] == '.':
                    name = cave_map[r][c] + cave_map[r][c+1]
                    name = ''.join(sorted(name))
                else:
                    continue
                if name in portals_dict:
                    portals_dict[name] = [portals_dict[name], (r,c)]
                else:
                    portals_dict[name] = (r,c)
    return portals_dict

def check_surroundings(pos):
    

def walk_maze(cave_map, dict_of_portals, start, goal):
    queue = collections.deque([(start,0)])
    while queue:
        (pos, distance) = queue.popleft()
        for next_vert in set(graph[vertex])-set(path):
            if next_vert == goal:
                yield path + [next_vert]
            else:
                queue.append((next_vert, path + [next_vert]))


def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next_vert in set(graph[vertex])-set(path):
            if next_vert == goal:
                yield path + [next_vert]
            else:
                queue.append((next_vert, path + [next_vert]))

cave_map = read_map('input20.txt')
portals = find_portals(cave_map)
print(portals)

#print(' '.isupper())