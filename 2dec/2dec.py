#!python3

def execute_one_op(sequence_index):
    opcode = sequence[sequence_index]
    if opcode == 99:
        print("Program halted")
        print(sequence[0])
        return False

    arg1 = sequence[sequence[sequence_index+1]]
    arg2 = sequence[sequence[sequence_index+2]]
    result_addr = sequence[sequence_index+3]

    if opcode == 1:
        sequence[result_addr] = arg1 + arg2
        return True
    elif opcode == 2:
        sequence[result_addr] = arg1 * arg2
        return True
    else:
        print("Something went wrong!")
        return False

with open('input2.txt') as input_file:
    intcode = input_file.read().strip().split(',')
    sequence = [int(i) for i in intcode]

# First task
sequence[1] = 12
sequence[2] = 2

sequence_index = 0
keep_going = True
while keep_going:
    keep_going = execute_one_op(sequence_index)
    sequence_index += 4
