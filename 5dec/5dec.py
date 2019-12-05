#!python3

class IntcodeComputer:
    def __init__(self):
        self.orig_sequence = []

    def read_input(self, file):
        with open(file) as input_file:
            intcode = input_file.read().strip().split(',')
            sequence_orig = [int(i) for i in intcode]
        self.orig_sequence = sequence_orig

    def get_copy_of_sequence(self):
        return self.orig_sequence.copy()

    def handle_opcode(self, op):
        str_opcode = str(op).zfill(5)
        opcode = int(str_opcode[-2:])
        arg3_mode = int(str_opcode[0])
        arg2_mode = int(str_opcode[1])
        arg1_mode = int(str_opcode[2])
        return opcode, arg1_mode, arg2_mode, arg3_mode

    def execute_one_op(self, sequence, sequence_index):
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
            value = input("Give your input: ") 
            arg1 = sequence[sequence_index+1]
            sequence[arg1] = int(value)
            return sequence_index + 2
        elif opcode == 4:
            arg1 = sequence_index+1 if arg1_mode else sequence[sequence_index+1]
            print("Output: {}".format(sequence[arg1]))
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

    def execute_complete_program(self, seq):
        seq_index = 0
        
        while seq_index >= 0:
            seq_index = self.execute_one_op(seq, seq_index)

        if seq_index == -1:
            print("Terminating...")
            return seq[0]
        else:
            print("Something went wrong!")
            return -1


def first_task():
    computer = IntcodeComputer()
    computer.read_input('input5.txt')
    sequence = computer.get_copy_of_sequence()
    computer.execute_complete_program(sequence)

def test_task2():
    computer = IntcodeComputer()
    computer.read_input('test.txt')
    sequence = computer.get_copy_of_sequence()
    computer.execute_complete_program(sequence)



first_task()
