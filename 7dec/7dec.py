#!python3
import itertools

class IntcodeComputer:
    def __init__(self):
        self.sequence = []
        self.inputs = []
        self.output = -1
        self.which_input = 0
        self.return_code = 0
        self.sequence_index = 0

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
            return -1, sequence_index
        elif opcode == 1:
            arg1 = sequence[sequence_index+1] if arg1_mode else sequence[sequence[sequence_index+1]]
            arg2 = sequence[sequence_index+2] if arg2_mode else sequence[sequence[sequence_index+2]]
            result_addr = sequence[sequence_index+3]
            sequence[result_addr] = arg1 + arg2
            return 1, sequence_index + 4
        elif opcode == 2:
            arg1 = sequence[sequence_index+1] if arg1_mode else sequence[sequence[sequence_index+1]]
            arg2 = sequence[sequence_index+2] if arg2_mode else sequence[sequence[sequence_index+2]]
            result_addr = sequence[sequence_index+3]
            sequence[result_addr] = arg1 * arg2
            return 1, sequence_index + 4
        elif opcode == 3:
            value = self.inputs[self.which_input]
            self.which_input = self.which_input + 1 if self.which_input == 0 else self.which_input 
            arg1 = sequence[sequence_index+1]
            sequence[arg1] = int(value)
            return 1, sequence_index + 2
        elif opcode == 4:
            arg1 = sequence_index+1 if arg1_mode else sequence[sequence_index+1]
            self.output = sequence[arg1]
            return -2, sequence_index + 2
        elif opcode == 5:
            arg1 = sequence[sequence_index+1] if arg1_mode else sequence[sequence[sequence_index+1]]
            arg2 = sequence[sequence_index+2] if arg2_mode else sequence[sequence[sequence_index+2]]
            if arg1 != 0:
                return 1, arg2
            else:
                return 1, sequence_index + 3
        elif opcode == 6:
            arg1 = sequence[sequence_index+1] if arg1_mode else sequence[sequence[sequence_index+1]]
            arg2 = sequence[sequence_index+2] if arg2_mode else sequence[sequence[sequence_index+2]]
            if arg1 == 0:
                return 1, arg2
            else:
                return 1, sequence_index + 3
        elif opcode == 7:
            arg1 = sequence[sequence_index+1] if arg1_mode else sequence[sequence[sequence_index+1]]
            arg2 = sequence[sequence_index+2] if arg2_mode else sequence[sequence[sequence_index+2]]
            result_addr = sequence[sequence_index+3]
            if arg1 < arg2:
                sequence[result_addr] = 1
            else:
                sequence[result_addr] = 0
            return 1, sequence_index + 4
        elif opcode == 8:
            arg1 = sequence[sequence_index+1] if arg1_mode else sequence[sequence[sequence_index+1]]
            arg2 = sequence[sequence_index+2] if arg2_mode else sequence[sequence[sequence_index+2]]
            result_addr = sequence[sequence_index+3]
            if arg1 == arg2:
                sequence[result_addr] = 1
            else:
                sequence[result_addr] = 0
            return 1, sequence_index + 4
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
            #print("Terminating...")
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

    print("First output: {}".format(output))

def second_task():
    output = 0
    phase_settings = [5,6,7,8,9]
    all_combinations = list(itertools.permutations(phase_settings, 5))
    for combination in all_combinations:
        amplifiers = []
        for i in range(0,6):
            amplifier = IntcodeComputer()
            amplifier.read_input('input7.txt')
            amplifiers.append(amplifier)
        last_amp_terminated = False
        inputs = [0, 0]
        while not last_amp_terminated:
            amp_nr = 0
            for i in combination:
                inputs[0] = i
                amplifier = amplifiers[amp_nr]
                amplifier.set_input_parameters(inputs[0], inputs[1])
                return_code = amplifier.execute_complete_program()
                if return_code == 2:
                    out = amplifier.get_output()
                    inputs[1] = out

                if return_code == 1 and amp_nr == 4:
                    out = amplifier.get_output()
                    last_amp_terminated = True

                amp_nr = amp_nr + 1 if amp_nr < 4 else 0

        output = out if out > output else output

    print("Second output: {}".format(output))

first_task()
second_task()
