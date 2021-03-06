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
        self.complete_input = []
        self.input_index = 0

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
            value = self.complete_input[self.input_index]
            self.input_index += 1
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

def first_task():
    ASCII = IntcodeComputer()
    ASCII.read_input('input17.txt')
    scaffold_map = ''
    scaffold_positions = []
    y_pos = 0
    x_pos = 0

    terminated = False
    while not terminated:
        return_code = ASCII.execute_complete_program()
        if return_code == 1:
            terminated = True
            continue

        output = ASCII.get_output()
        if output == 35:
            scaffold_positions.append((x_pos,y_pos))

        x_pos += 1
        
        if output == 10:
            y_pos += 1
            x_pos = 0
        
        scaffold_map = scaffold_map + chr(output)

    with open("scaffold_map.txt", "w") as text_file:
        text_file.write(scaffold_map)

    intersects = []
    for scaf in scaffold_positions:
        check_scaf1 = (scaf[0]+1,scaf[1])
        check_scaf2 = (scaf[0]-1,scaf[1])
        check_scaf3 = (scaf[0],scaf[1]+1)
        check_scaf4 = (scaf[0],scaf[1]-1)
        if check_scaf1 in scaffold_positions and \
           check_scaf2 in scaffold_positions and \
           check_scaf3 in scaffold_positions and \
           check_scaf4 in scaffold_positions:
           intersects.append(scaf)

    intersects_sum = 0

    for intersect in intersects:
        intersects_sum += intersect[0] * intersect[1]

    print(intersects_sum)


def second_task():
    ASCII = IntcodeComputer()
    ASCII.read_input('input17.txt')
    ASCII.sequence[0] = 2
    scaffold_map = ''
    movement_routine = 'A,B,B,C,A,B,C,A,B,C\n'
    A_seq = 'L,6,R,12,L,4,L,6\n'
    B_seq = 'R,6,L,6,R,12\n'
    C_seq = 'L,6,L,10,L,10,R,6\n'
    video_yn = 'n\n'
    path_input = []
    for st in movement_routine:
        path_input.append(ord(st))
    for st in A_seq:
        path_input.append(ord(st))
    for st in B_seq:
        path_input.append(ord(st))
    for st in C_seq:
        path_input.append(ord(st))
    for st in video_yn:
        path_input.append(ord(st))

    # A little special solution for handling the inputs
    ASCII.complete_input = path_input
    
    terminated = False
    while not terminated:
        return_code = ASCII.execute_complete_program()
        output = ASCII.get_output()
        if return_code == 1:
            terminated = True
            continue

        if output > 255:
            scaffold_map = scaffold_map + 'Dust: ' + str(output)
        else:        
            scaffold_map = scaffold_map + chr(output)

    print(scaffold_map)

second_task()
