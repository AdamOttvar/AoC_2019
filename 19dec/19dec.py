#!python3

class IntcodeComputer:
    def __init__(self):
        self.orig_sequence = []
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
        self.orig_sequence = sequence_orig.copy()
        self.sequence = sequence_orig.copy()

    def reset(self):
        self.sequence = self.orig_sequence.copy()
        self.input = 0
        self.output = -1
        self.which_input = 0
        self.return_code = 0
        self.sequence_index = 0
        self.relative_base = 0

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
            return -3, sequence_index + 2
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
        elif code == -3:
            #print("Read input...")
            self.sequence_index = seq_index
            return 3
        else:
            print("Something went wrong!")
            return -1

def check_one_position(computer, x_coord, y_coord):
    computer.reset()
    computer.input = x_coord
    return_code = computer.execute_complete_program()
    computer.input = y_coord
    return_code = computer.execute_complete_program()
    return_code = computer.execute_complete_program()
    return computer.get_output()


def first_task():
    drone_system = IntcodeComputer()
    drone_system.read_input('input19.txt')
    beam_map = []

    nbr_of_beam = 0

    for y_pos in range(0,50):
        row = []
        for x_pos in range(0,50):
            output = check_one_position(drone_system, x_pos, y_pos)
            if output:
                nbr_of_beam += 1
                row.append('#')
            else:
                row.append('.')
        beam_map.append(row)

    for row in beam_map:
        print(''.join(row))

    print("Number of points: {}".format(nbr_of_beam))


def second_task():
    drone_system = IntcodeComputer()
    drone_system.read_input('input19.txt')

    upper_point = [824, 1394]
    lower_point = [854, 1127]

    print("Point: {}".format(upper_point))
    print("Point: {}".format(lower_point))

    found = False
    x_coord = 600
    while not found:
        y_max = int(x_coord*float(upper_point[1])/float(upper_point[0]))
        y_min = int(x_coord*float(lower_point[1])/float(lower_point[0]))
        for y_coord in range(y_min, y_max):
            x_check = check_one_position(drone_system, x_coord+99, y_coord)
            y_check = check_one_position(drone_system, x_coord, y_coord+99)
            if x_check and y_check:
                found = True
                print("Point: {}, {}".format(x_coord,y_coord))
                print("Answer: {}".format(x_coord*10000+y_coord))
                break
        x_coord += 1

          
second_task()

        