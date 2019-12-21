#!python3
import collections

def read_map(file):
    cave_map = []
    with open(file) as input_file:
        for line in input_file:
            cave_map.append(list(line.strip()))
    return cave_map.copy()

def check_passage(x_pos, y_pos, cave_map):
    ok_passages = []
    # Check CW
    if cave_map[y_pos-1][x_pos] != '#':
        ok_passages.append((x_pos, y_pos-1))
    if cave_map[y_pos][x_pos+1] != '#':
        ok_passages.append((x_pos+1, y_pos))
    if cave_map[y_pos+1][x_pos] != '#':
        ok_passages.append((x_pos, y_pos+1))
    if cave_map[y_pos][x_pos-1] != '#':
        ok_passages.append((x_pos-1, y_pos))
    return ok_passages.copy()

def analyze_map(cave_map):
    height = len(cave_map)
    width = len(cave_map[0])
    all_keys = set()
    for y in range(0, height):
        for x in range(0,width):
            if cave_map[y][x] == '@':
                start_pos = (x,y)
            if cave_map[y][x].islower():
                all_keys.add(cave_map[y][x])
    return start_pos, all_keys

def bfs_explore(start_pos, cave_map, all_keys):
    #start_pos = (x,y,0,set())
    visited = set()
    queue = collections.deque([(start_pos[0],start_pos[1],0,set())])
    while queue:
        vertex = queue.popleft()
        key = (vertex[0], vertex[1], tuple(sorted(vertex[3])))
        if key in visited:
            continue
        visited.add(key)

        if cave_map[vertex[1]][vertex[0]].isupper() and \
           cave_map[vertex[1]][vertex[0]].lower() not in vertex[3]:
           continue

        current_keys = vertex[3].copy()
        if cave_map[vertex[1]][vertex[0]].islower():
            current_keys.add(cave_map[vertex[1]][vertex[0]])
            if current_keys == all_keys:
                print(current_keys)
                print("Goal: ")
                print(vertex[2])
                break

        valid_passages = check_passage(vertex[0],vertex[1],cave_map)
        for passage in valid_passages:
            new_distance = vertex[2] + 1
            queue.append((passage[0],passage[1],new_distance,current_keys))

    #print(visited)

cave_map = read_map('input18.txt')
start_pos, all_keys = analyze_map(cave_map)
print(all_keys)
bfs_explore(start_pos, cave_map, all_keys)
#print(cave_map[35][1].islower())