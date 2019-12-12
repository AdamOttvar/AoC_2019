#!python3

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

def print_panels(panels):
    printed_panels = []
    all_panels = [*panels]
    x_values = [x[0] for x in all_panels]
    max_x = max(x_values)
    min_x = min(x_values)
    y_values = [x[1] for x in all_panels]
    max_y = max(y_values)
    min_y = min(y_values)
    row = ['.']*(max_x-min_x+1)

    for i in range(max_y, abs(min_y)+1):
        printed_panels.append(row.copy())

    for panel in all_panels:
        panel_color = '#' if panels[panel] else '.'
        printed_panels[abs(panel[1])][panel[0]] = panel_color

    for row in printed_panels:
        print(''.join(row))



def first_task():
    panel_map = {}
    robot_position = (0, 0)
    headings = ['U', 'R', 'D', 'L']
    robot_heading = 'U'
    panel_color = 0
    panel_map[robot_position] = panel_color
    paint_robot = IntcodeComputer()
    paint_robot.read_input('input11.txt')

    terminated = False
    while not terminated:
        if robot_position in panel_map:
            panel_color = panel_map[robot_position]
        else:
            panel_color = 0
            panel_map[robot_position] = panel_color

        paint_robot.input = panel_color

        return_code = paint_robot.execute_complete_program()
        if return_code == 1:
            terminated = True
            continue

        color_to_paint = paint_robot.get_output()
        panel_map[robot_position] = color_to_paint

        return_code = paint_robot.execute_complete_program()
        if return_code == 1:
            terminated = True
            continue

        direction_to_move = paint_robot.get_output()
        if robot_heading == 'U':
            robot_heading = 'R' if direction_to_move else 'L'
        elif robot_heading == 'R':
            robot_heading = 'D' if direction_to_move else 'U'
        elif robot_heading == 'D':
            robot_heading = 'L' if direction_to_move else 'R'
        elif robot_heading == 'L':
            robot_heading = 'U' if direction_to_move else 'D'

        if robot_heading == 'U':
            robot_position = (robot_position[0],robot_position[1]+1)
            #robot_position[1] += 1
        elif robot_heading == 'R':
            robot_position = (robot_position[0]+1,robot_position[1])
            #robot_position[0] += 1
        elif robot_heading == 'D':
            robot_position = (robot_position[0],robot_position[1]-1)
            #robot_position[1] -= 1
        elif robot_heading == 'L':
            robot_position = (robot_position[0]-1,robot_position[1])
            #robot_position[0] -= 1

    print(len(panel_map))

def second_task():
    panel_map = {}
    robot_position = (0, 0)
    headings = ['U', 'R', 'D', 'L']
    robot_heading = 'U'
    panel_color = 1
    panel_map[robot_position] = panel_color
    paint_robot = IntcodeComputer()
    paint_robot.read_input('input11.txt')

    terminated = False
    while not terminated:
        if robot_position in panel_map:
            panel_color = panel_map[robot_position]
        else:
            panel_color = 0
            panel_map[robot_position] = panel_color

        paint_robot.input = panel_color

        return_code = paint_robot.execute_complete_program()
        if return_code == 1:
            terminated = True
            continue

        color_to_paint = paint_robot.get_output()
        panel_map[robot_position] = color_to_paint

        return_code = paint_robot.execute_complete_program()
        if return_code == 1:
            terminated = True
            continue

        direction_to_move = paint_robot.get_output()
        if robot_heading == 'U':
            robot_heading = 'R' if direction_to_move else 'L'
        elif robot_heading == 'R':
            robot_heading = 'D' if direction_to_move else 'U'
        elif robot_heading == 'D':
            robot_heading = 'L' if direction_to_move else 'R'
        elif robot_heading == 'L':
            robot_heading = 'U' if direction_to_move else 'D'

        if robot_heading == 'U':
            robot_position = (robot_position[0],robot_position[1]+1)
            #robot_position[1] += 1
        elif robot_heading == 'R':
            robot_position = (robot_position[0]+1,robot_position[1])
            #robot_position[0] += 1
        elif robot_heading == 'D':
            robot_position = (robot_position[0],robot_position[1]-1)
            #robot_position[1] -= 1
        elif robot_heading == 'L':
            robot_position = (robot_position[0]-1,robot_position[1])
            #robot_position[0] -= 1

    print(len(panel_map))
    print_panels(panel_map)

second_task()
