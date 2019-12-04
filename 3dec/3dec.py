#!python3
def split_instruction(instruction):
    head = instruction.rstrip('0123456789')
    tail = instruction[len(head):]
    return head, int(tail)

def visit_coord(coordinate, wire_nbr, start_coord):
    global min_distance
    if str(coordinate) in global_schema:
        if global_schema[str(coordinate)] == wire_nbr:
            global_schema[str(coordinate)] = wire_nbr
            return False
        elif global_schema[str(coordinate)] == 99:
            return True
        else:
            global_schema[str(coordinate)] = 99
            distance = abs(start_coord[0] - coordinate[0])+abs(start_coord[1] - coordinate[1])
            min_distance = distance if distance < min_distance else min_distance
            return False
    else:
        global_schema[str(coordinate)] = wire_nbr
        return False


def run_one_instruction(instr, curr_coord, wire_nbr, start_coord):
    direction = instr[0]
    steps = instr[1]
    if direction == "U":
        for i in range(curr_coord[1]+1, curr_coord[1]+1+steps):
            curr_coord = [curr_coord[0], i]
            visit_coord(curr_coord, wire_nbr, start_coord)

    elif direction == "D":
        for i in range(curr_coord[1]-1, curr_coord[1]-1-steps, -1):
            curr_coord = [curr_coord[0], i]
            visit_coord(curr_coord, wire_nbr, start_coord)

    elif direction == "R":
        for i in range(curr_coord[0]+1, curr_coord[0]+1+steps):
            curr_coord = [i, curr_coord[1]]
            visit_coord(curr_coord, wire_nbr, start_coord)

    elif direction == "L":
        for i in range(curr_coord[0]-1, curr_coord[0]-1-steps, -1):
            curr_coord = [i, curr_coord[1]]
            visit_coord(curr_coord, wire_nbr, start_coord)

    else:
        print("Not a correct instruction")

    return curr_coord


def run_wire(wire_instructions, start_coord, wire_nbr):
    current_coordinate = start_coord
    for instruction in wire_instructions:
        current_coordinate = run_one_instruction(instruction, current_coordinate, wire_nbr, start_coord)

def run_wire_and_count(wire_instructions, start_coord, wire_nbr):
    global global_schema_length
    curr_coord = start_coord
    wire_counter = 0
    for instr in wire_instructions:
        direction = instr[0]
        steps = instr[1]
        if direction == "U":
            for i in range(curr_coord[1]+1, curr_coord[1]+1+steps):
                wire_counter += 1
                curr_coord = [curr_coord[0], i]
                intersect = visit_coord(curr_coord, wire_nbr, start_coord)
                if intersect:
                    if wire_nbr == 1:
                        global_schema_length[str(curr_coord)] = [wire_counter, 0]
                    else:
                        global_schema_length[str(curr_coord)][1] = wire_counter

        elif direction == "D":
            for i in range(curr_coord[1]-1, curr_coord[1]-1-steps, -1):
                wire_counter += 1
                curr_coord = [curr_coord[0], i]
                intersect = visit_coord(curr_coord, wire_nbr, start_coord)
                if intersect:
                    if wire_nbr == 1:
                        global_schema_length[str(curr_coord)] = [wire_counter, 0]
                    else:
                        global_schema_length[str(curr_coord)][1] = wire_counter

        elif direction == "R":
            for i in range(curr_coord[0]+1, curr_coord[0]+1+steps):
                wire_counter += 1
                curr_coord = [i, curr_coord[1]]
                intersect = visit_coord(curr_coord, wire_nbr, start_coord)
                if intersect:
                    if wire_nbr == 1:
                        global_schema_length[str(curr_coord)] = [wire_counter, 0]
                    else:
                        global_schema_length[str(curr_coord)][1] = wire_counter

        elif direction == "L":
            for i in range(curr_coord[0]-1, curr_coord[0]-1-steps, -1):
                wire_counter += 1
                curr_coord = [i, curr_coord[1]]
                intersect = visit_coord(curr_coord, wire_nbr, start_coord)
                if intersect:
                    if wire_nbr == 1:
                        global_schema_length[str(curr_coord)] = [wire_counter, 0]
                    else:
                        global_schema_length[str(curr_coord)][1] = wire_counter

        else:
            print("Not a correct instruction")


def first_task():
    with open('input3.txt') as input_file:
        wire_paths = input_file.read().strip().split()

    for index in range(len(wire_paths)):
        wire_paths[index] = [split_instruction(instruction) for instruction in wire_paths[index].split(',')]

    """
    wire1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
    wire2 = 'U62,R66,U55,R34,D71,R55,D58,R83'
    wire_path1 = [split_instruction(instruction) for instruction in wire1.split(',')]
    wire_path2 = [split_instruction(instruction) for instruction in wire2.split(',')]
    wire_paths = [wire_path1, wire_path2]
    """
    run_wire(wire_paths[0], start_coord, 1)
    run_wire(wire_paths[1], start_coord, 2)
    print(min_distance)

def second_task():
    with open('input3.txt') as input_file:
        wire_paths = input_file.read().strip().split()

    for index in range(len(wire_paths)):
        wire_paths[index] = [split_instruction(instruction) for instruction in wire_paths[index].split(',')]

    """
    wire1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
    wire2 = 'U62,R66,U55,R34,D71,R55,D58,R83'
    wire_path1 = [split_instruction(instruction) for instruction in wire1.split(',')]
    wire_path2 = [split_instruction(instruction) for instruction in wire2.split(',')]
    wire_paths = [wire_path1, wire_path2]
    """
    run_wire_and_count(wire_paths[0], start_coord, 1)
    run_wire_and_count(wire_paths[1], start_coord, 2)
    print(min_distance)

global_schema = {}
global_schema_length = {}
start_coord = [0, 0]
min_distance = 99999999999
min_length = 99999999999
first_task()
second_task()
for intersect in global_schema_length:
    values = global_schema_length[intersect]
    length = values[0] + values[1]
    min_length = length if length < min_length else min_length
print(min_length)
