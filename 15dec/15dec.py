#!python3
import collections

def plot_path(droid_points, wall_points, oxygen_point, path_points):
    import matplotlib.pyplot as plt

    droid_x_pos =  [x[0] for x in droid_points]
    droid_y_pos =  [x[1] for x in droid_points]
    wall_x_pos =  [x[0] for x in wall_points]
    wall_y_pos =  [x[1] for x in wall_points]
    path_x_pos =  [x[0] for x in path_points]
    path_y_pos =  [x[1] for x in path_points]
    fig=plt.figure()
    ax=fig.add_axes([0,0,1,1])
    ax.scatter(wall_x_pos, wall_y_pos, color='r')
    ax.scatter(droid_x_pos, droid_y_pos, color='k')
    ax.scatter(path_x_pos, path_y_pos, color='g')
    ax.scatter(oxygen_point[0], oxygen_point[1], color='b')
    plt.show()


class IntcodeComputer:
    def __init__(self):
        self.sequence = []
        self.input = 0
        self.output = -1
        self.which_input = 0
        self.return_code = 0
        self.sequence_index = 0
        self.relative_base = 0

    def read_input(self, file):
        with open(file) as input_file:
            intcode = input_file.read().strip().split(',')
            sequence_orig = [int(i) for i in intcode]
        self.sequence = sequence_orig.copy()

    def get_output(self):
        return self.output

    def get_copy_of_sequence(self):
        return self.orig_sequence.copy()

    def handle_opcode(self, op):
        str_opcode = str(op).zfill(5)
        opcode = int(str_opcode[-2:])
        arg3_mode = int(str_opcode[0])
        arg2_mode = int(str_opcode[1])
        arg1_mode = int(str_opcode[2])
        return opcode, arg1_mode, arg2_mode, arg3_mode

    def handle_memory(self, index):
        if len(self.sequence) <= index:
            fill_array = [0]*(index + 1 - len(self.sequence))
            self.sequence.extend(fill_array)

    def get_parameter_for_mode(self, index, mode, write=False):
        sequence = self.sequence
        if mode == 0:
            new_index = sequence[index]
            self.handle_memory(new_index)
            if write:
                return new_index
            return sequence[new_index]
        elif mode == 1:
            self.handle_memory(index)
            if write:
                return new_index
            return sequence[index]
        elif mode == 2:
            new_index = sequence[index]+self.relative_base
            self.handle_memory(new_index)
            if write:
                return new_index
            return sequence[new_index]
        else:
            print("Parameter mode not recognized")

    def execute_one_op(self, sequence_index):
        sequence = self.sequence
        opcode = sequence[sequence_index]
        opcode, arg1_mode, arg2_mode, arg3_mode = self.handle_opcode(opcode)
        if opcode == 99:
            return -1, sequence_index
        elif opcode == 1:
            arg1 = self.get_parameter_for_mode(sequence_index+1, arg1_mode)
            arg2 = self.get_parameter_for_mode(sequence_index+2, arg2_mode)
            result_addr = self.get_parameter_for_mode(sequence_index+3, arg3_mode, True)
            self.handle_memory(result_addr)
            sequence[result_addr] = arg1 + arg2
            return 1, sequence_index + 4
        elif opcode == 2:
            arg1 = self.get_parameter_for_mode(sequence_index+1, arg1_mode)
            arg2 = self.get_parameter_for_mode(sequence_index+2, arg2_mode)
            result_addr = self.get_parameter_for_mode(sequence_index+3, arg3_mode, True)
            self.handle_memory(result_addr)
            sequence[result_addr] = arg1 * arg2
            return 1, sequence_index + 4
        elif opcode == 3:
            value = self.input
            arg1 = self.get_parameter_for_mode(sequence_index+1, arg1_mode, True)
            sequence[arg1] = int(value)
            return 1, sequence_index + 2
        elif opcode == 4:
            arg1 = self.get_parameter_for_mode(sequence_index+1, arg1_mode)
            self.output = arg1
            return -2, sequence_index + 2
        elif opcode == 5:
            arg1 = self.get_parameter_for_mode(sequence_index+1, arg1_mode)
            arg2 = self.get_parameter_for_mode(sequence_index+2, arg2_mode)
            if arg1 != 0:
                return 1, arg2
            else:
                return 1, sequence_index + 3
        elif opcode == 6:
            arg1 = self.get_parameter_for_mode(sequence_index+1, arg1_mode)
            arg2 = self.get_parameter_for_mode(sequence_index+2, arg2_mode)
            if arg1 == 0:
                return 1, arg2
            else:
                return 1, sequence_index + 3
        elif opcode == 7:
            arg1 = self.get_parameter_for_mode(sequence_index+1, arg1_mode)
            arg2 = self.get_parameter_for_mode(sequence_index+2, arg2_mode)
            result_addr = self.get_parameter_for_mode(sequence_index+3, arg3_mode, True)
            self.handle_memory(result_addr)
            if arg1 < arg2:
                sequence[result_addr] = 1
            else:
                sequence[result_addr] = 0
            return 1, sequence_index + 4
        elif opcode == 8:
            arg1 = self.get_parameter_for_mode(sequence_index+1, arg1_mode)
            arg2 = self.get_parameter_for_mode(sequence_index+2, arg2_mode)
            result_addr = self.get_parameter_for_mode(sequence_index+3, arg3_mode, True)
            self.handle_memory(result_addr)
            if arg1 == arg2:
                sequence[result_addr] = 1
            else:
                sequence[result_addr] = 0
            return 1, sequence_index + 4
        elif opcode == 9:
            arg1 = self.get_parameter_for_mode(sequence_index+1, arg1_mode)
            self.relative_base = self.relative_base + arg1
            return 1, sequence_index + 2
        else:
            print(opcode)
            print("seq ind: {}".format(sequence_index))
            print(sequence)
            return -99, sequence_index

    def execute_complete_program(self):
        seq_index = self.sequence_index
        code = 0
        
        while code >= 0:
            code, seq_index = self.execute_one_op(seq_index)

        if code == -1:
            print("Terminating...")
            self.sequence_index = 0
            return 1
        elif code == -2:
            #print("Got output...")
            self.sequence_index = seq_index
            return 2
        else:
            print("Something went wrong!")
            return -1

def update_droid_position(position,direction,droid_map,graph):
    parent_position = (position[0],position[1])
    if direction == 1:
        position[1] += 1
    elif direction == 2:
        position[1] -= 1
    elif direction == 3:
        position[0] -= 1
    elif direction == 4:
        position[0] += 1
    else:
        print("Unknown direction!")
    droid_map.append((position[0],position[1]))
    if parent_position in graph:
        graph[parent_position].append((position[0],position[1]))
    else:
        graph[parent_position] = [(position[0],position[1])]

def update_wall_position(position,direction,wall_map):
    if direction == 1:
        wall_position = [position[0], position[1] + 1]
    elif direction == 2:
        wall_position = [position[0], position[1] - 1]
    elif direction == 3:
        wall_position = [position[0] - 1, position[1]]
    elif direction == 4:
        wall_position = [position[0] + 1, position[1]]
    else:
        print("Unknown direction!")
    wall_map.append((wall_position[0],wall_position[1]))

def set_oxygen_position(position,direction,graph):
    parent_position = (position[0],position[1])
    if direction == 1:
        position[1] += 1
    elif direction == 2:
        position[1] -= 1
    elif direction == 3:
        position[0] -= 1
    elif direction == 4:
        position[0] += 1
    else:
        print("Unknown direction!")
    graph[parent_position] = [(position[0],position[1])]
    return position.copy() 

def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next_vert in set(graph[vertex])-set(path):
            if next_vert == goal:
                yield path + [next_vert]
            else:
                queue.append((next_vert, path + [next_vert]))

def first_task():
    repair_droid = IntcodeComputer()
    repair_droid.read_input('input15.txt')
    nbr_of_commands = 0
    droid_map = []
    droid_graph = {}
    droid_position = [0,0]
    droid_map.append(droid_position.copy())
    wall_positions = []
    direction = 1
    oxygen_position = [0,0]
    # 1->4 2->3 3->1 4->2
    right_direction = {1:4, 2:3, 3:1, 4:2}
    # 1->4 2->3 3->1 4->2
    left_direction = {1:3, 2:4, 3:2, 4:1}

    terminated = False
    while not terminated:
        direction = right_direction[direction]
        repair_droid.input = direction
        return_code = repair_droid.execute_complete_program()
        nbr_of_commands += 1
        output = repair_droid.get_output()
        if output == 1:
            update_droid_position(droid_position,direction,droid_map,droid_graph)
        elif output == 0:
            update_wall_position(droid_position,direction,wall_positions)
            direction = left_direction[direction]
            repair_droid.input = direction
            return_code = repair_droid.execute_complete_program()
            nbr_of_commands += 1
            output = repair_droid.get_output()
            if output == 1:
                update_droid_position(droid_position,direction,droid_map,droid_graph)
            elif output == 0:
                update_wall_position(droid_position,direction,wall_positions)
                direction = left_direction[direction]
                repair_droid.input = direction
                return_code = repair_droid.execute_complete_program()
                nbr_of_commands += 1
                output = repair_droid.get_output()
                if output == 1:
                    update_droid_position(droid_position,direction,droid_map,droid_graph)
            elif output == 2:
                oxygen_position = set_oxygen_position(droid_position,direction,droid_graph)
                droid_map.append((oxygen_position[0],oxygen_position[1]))

        elif output == 2:
            oxygen_position = set_oxygen_position(droid_position,direction,droid_graph)
            droid_map.append((oxygen_position[0],oxygen_position[1]))

        if droid_position == [0,0]:
            terminated = True

    path = list(bfs_paths(droid_graph, (0,0), (oxygen_position[0],oxygen_position[1])))[0] # [['A', 'C', 'F'], ['A', 'B', 'E', 'F']]
    plot_path(droid_map, wall_positions, oxygen_position, path)
    print(len(path)-1)


def second_task():
    repair_droid = IntcodeComputer()
    repair_droid.read_input('input15.txt')
    nbr_of_commands = 0
    droid_map = []
    droid_graph = {}
    droid_position = [0,0]
    droid_map.append(droid_position.copy())
    wall_positions = []
    direction = 1
    oxygen_position = [0,0]
    # 1->4 2->3 3->1 4->2
    right_direction = {1:4, 2:3, 3:1, 4:2}
    # 1->4 2->3 3->1 4->2
    left_direction = {1:3, 2:4, 3:2, 4:1}

    terminated = False
    while not terminated:
        direction = right_direction[direction]
        repair_droid.input = direction
        return_code = repair_droid.execute_complete_program()
        nbr_of_commands += 1
        output = repair_droid.get_output()
        if output == 1:
            update_droid_position(droid_position,direction,droid_map,droid_graph)
        elif output == 0:
            update_wall_position(droid_position,direction,wall_positions)
            direction = left_direction[direction]
            repair_droid.input = direction
            return_code = repair_droid.execute_complete_program()
            nbr_of_commands += 1
            output = repair_droid.get_output()
            if output == 1:
                update_droid_position(droid_position,direction,droid_map,droid_graph)
            elif output == 0:
                update_wall_position(droid_position,direction,wall_positions)
                direction = left_direction[direction]
                repair_droid.input = direction
                return_code = repair_droid.execute_complete_program()
                nbr_of_commands += 1
                output = repair_droid.get_output()
                if output == 1:
                    update_droid_position(droid_position,direction,droid_map,droid_graph)
            elif output == 2:
                oxygen_position = set_oxygen_position(droid_position,direction,droid_graph)
                droid_map.append((oxygen_position[0],oxygen_position[1]))

        elif output == 2:
            oxygen_position = set_oxygen_position(droid_position,direction,droid_graph)
            droid_map.append((oxygen_position[0],oxygen_position[1]))

        if droid_position == [0,0]:
            terminated = True

    path = list(bfs_paths(droid_graph, (0,0), (oxygen_position[0],oxygen_position[1])))[0] # [['A', 'C', 'F'], ['A', 'B', 'E', 'F']]
    plot_path(droid_map, wall_positions, oxygen_position, path)
    print(len(path)-1)

first_task()
second_task()
