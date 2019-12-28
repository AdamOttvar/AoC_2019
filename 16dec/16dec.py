#!python3

def first_task():
    with open('input16.txt') as input_file:
        signal_input = input_file.read().strip()

    signal = [int(x) for x in signal_input]
    output_list = [0]*len(signal)
    base_pattern = [0, 1, 0, -1]

    nbr_of_phases = 100
    for phase in range(0,nbr_of_phases):
        for index in range(0,len(output_list)):
            repeated_pattern = []
            for index2 in base_pattern:
                repeat = [base_pattern[index2]]*(index+1)
                repeated_pattern.extend(repeat)
            pattern = repeated_pattern[1:]
            while len(pattern) < len(output_list):
                pattern.extend(repeated_pattern)
            pattern = pattern[0:len(output_list)]
            
            result = 0
            for index3 in range(0,len(signal)):
                result += pattern[index3]*signal[index3]

            output_list[index] = abs(result)%10

        signal = output_list.copy()

    print(output_list[:8])


def second_task():
    
    with open('input16.txt') as input_file:
        signal_input = input_file.read().strip()
    
    #signal_input = '69317163492948606335995924319873'
    #signal_input = '1111111111'
    message_start = int(''.join(str(x) for x in signal_input[:7]))
    signal = [int(x) for x in signal_input]
    signal = signal*10000
    output_list = [0]*len(signal)
    base_pattern = [0, 1, 0, -1]

    needed_index_start = 2*message_start - len(signal)

    nbr_of_phases = 100
    for phase in range(0,nbr_of_phases):
        print(phase)
        result = 0
        for index in range(len(output_list)-1, needed_index_start, -1):
            result += signal[index]
            output_list[index] = abs(result)%10

        signal = output_list.copy()

    print(message_start)
    print(output_list[message_start:message_start+8])

#first_task()
second_task()
