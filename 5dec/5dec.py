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

    def execute_one_op(self, sequence, sequence_index):
        opcode = sequence[sequence_index]
        if opcode == 99:
            return -1
        elif opcode == 1:
            arg1 = sequence[sequence[sequence_index+1]]
            arg2 = sequence[sequence[sequence_index+2]]
            result_addr = sequence[sequence_index+3]
            sequence[result_addr] = arg1 + arg2
            return sequence_index + 4
        elif opcode == 2:
            arg1 = sequence[sequence[sequence_index+1]]
            arg2 = sequence[sequence[sequence_index+2]]
            result_addr = sequence[sequence_index+3]
            sequence[result_addr] = arg1 * arg2
            return sequence_index + 4
        else:
            return -99

    def execute_complete_program(self, seq):
        seq_index = 0
        
        while seq_index >= 0:
            seq_index = self.execute_one_op(seq, seq_index)

        if seq_index == -1:
            return seq[0]
        else:
            print("Something went wrong!")
            return -1


def first_task():
    computer = IntcodeComputer()
    computer.read_input('input2.txt')
    sequence = computer.get_copy_of_sequence()
    sequence[1] = 12
    sequence[2] = 2
    first_answer = computer.execute_complete_program(sequence)
    print("=== First answer: ")
    print(first_answer)


def second_task():
    computer = IntcodeComputer()
    computer.read_input('input2.txt')
    list_of_nouns = range(100)
    list_of_verbs = range(100)
    keep_on_going = True

    for noun in list_of_nouns:
        for verb in list_of_verbs:
            sequence = computer.get_copy_of_sequence()
            sequence[1] = noun
            sequence[2] = verb
            second_answer = computer.execute_complete_program(sequence)
            
            if second_answer == 19690720:
                print("=== Second answer: ")
                print("Noun: {}   Verb: {}".format(noun, verb))
                print("Solution: {}".format(100 * noun + verb))
                keep_on_going = False
                break

        if not keep_on_going:
            break


first_task()
second_task()
