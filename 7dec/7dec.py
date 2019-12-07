#!python3
import itertools

class IntcodeComputer:
    def __init__(self):
        self.sequence = []
        self.inputs = []
        self.output = -1
        self.which_input = 0

    def read_input(self, file):
        with open(file) as input_file:
            intcode = input_file.read().strip().split(',')
            sequence_orig = [int(i) for i in intcode]
        self.sequence = sequence_orig.copy()

    def set_input_parameters(self, first, second):
        self.inputs = [first, second]

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

    def execute_one_op(self, sequence_index):
        sequence = self.sequence
        opcode = sequence[sequence_index]
        opcode, arg1_mode, arg2_mode, arg3_mode = self.handle_opcode(opcode)
        if opcode == 99:
            return -1
        elif opcode == 1:
            arg1 = sequence[sequence_index+1] if arg1_mode else sequence[sequence[sequence_index+1]]
            arg2 = sequence[sequence_index+2] if arg2_mode else sequence[sequence[sequence_index+2]]
            result_addr = sequence[sequence_index+3]
            sequence[result_addr] = arg1 + arg2
            return sequence_index + 4
        elif opcode == 2:
            arg1 = sequence[sequence_index+1] if arg1_mode else sequence[sequence[sequence_index+1]]
            arg2 = sequence[sequence_index+2] if arg2_mode else sequence[sequence[sequence_index+2]]
            result_addr = sequence[sequence_index+3]
            sequence[result_addr] = arg1 * arg2
            return sequence_index + 4
        elif opcode == 3:
            #value = input("Give your input: ")
            value = self.inputs[self.which_input]
            self.which_input += 1 
            arg1 = sequence[sequence_index+1]
            sequence[arg1] = int(value)
            return sequence_index + 2
        elif opcode == 4:
            arg1 = sequence_index+1 if arg1_mode else sequence[sequence_index+1]
            #print("Output: {}".format(sequence[arg1]))
            self.output = sequence[arg1]
            return sequence_index + 2
        elif opcode == 5:
            arg1 = sequence[sequence_index+1] if arg1_mode else sequence[sequence[sequence_index+1]]
            arg2 = sequence[sequence_index+2] if arg2_mode else sequence[sequence[sequence_index+2]]
            if arg1 != 0:
                return arg2
            else:
                return sequence_index + 3
        elif opcode == 6:
            arg1 = sequence[sequence_index+1] if arg1_mode else sequence[sequence[sequence_index+1]]
            arg2 = sequence[sequence_index+2] if arg2_mode else sequence[sequence[sequence_index+2]]
            if arg1 == 0:
                return arg2
            else:
                return sequence_index + 3
        elif opcode == 7:
            arg1 = sequence[sequence_index+1] if arg1_mode else sequence[sequence[sequence_index+1]]
            arg2 = sequence[sequence_index+2] if arg2_mode else sequence[sequence[sequence_index+2]]
            result_addr = sequence[sequence_index+3]
            if arg1 < arg2:
                sequence[result_addr] = 1
            else:
                sequence[result_addr] = 0
            return sequence_index + 4
        elif opcode == 8:
            arg1 = sequence[sequence_index+1] if arg1_mode else sequence[sequence[sequence_index+1]]
            arg2 = sequence[sequence_index+2] if arg2_mode else sequence[sequence[sequence_index+2]]
            result_addr = sequence[sequence_index+3]
            if arg1 == arg2:
                sequence[result_addr] = 1
            else:
                sequence[result_addr] = 0
            return sequence_index + 4
        else:
            print(opcode)
            print("seq ind: {}".format(sequence_index))
            print(sequence)
            return -99

    def execute_complete_program(self):
        seq_index = 0
        
        while seq_index >= 0:
            seq_index = self.execute_one_op(seq_index)

        if seq_index == -1:
            print("Terminating...")
            return self.sequence[0]
        else:
            print("Something went wrong!")
            return -1


def first_task():
    output = 0
    phase_setting = [0,1,2,3,4]
    all_combinations = list(itertools.permutations(phase_setting, 5))
    for combination in all_combinations:
        inputs = [0, 0]
        for i in combination:
            inputs[0] = i
            amplifier = IntcodeComputer()
            amplifier.read_input('input7.txt')
            amplifier.set_input_parameters(inputs[0], inputs[1])
            amplifier.execute_complete_program()
            out = amplifier.get_output()
            inputs[1] = out
        output = out if out > output else output

    print(output)

def second_task():
    amplifiers = []
    for i in range(0,6):
        amplifier = IntcodeComputer()
        amplifier.read_input('input7.txt')
        amplifiers.append(amplifier)

    output = 0
    phase_setting = [5,6,7,8,9]
    all_combinations = list(itertools.permutations(phase_setting, 5))
    for combination in all_combinations:
        inputs = [0, 0]
        for i in combination:
            inputs[0] = i
            amplifier = IntcodeComputer()
            amplifier.read_input('input7.txt')
            amplifier.set_input_parameters(inputs[0], inputs[1])
            amplifier.execute_complete_program()
            out = amplifier.get_output()
            inputs[1] = out
        output = out if out > output else output

    print(output)

first_task()
