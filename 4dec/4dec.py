#!python3

def check_combination(number):
    unique_digits = []
    previous_digit = 0
    for digit in [int(d) for d in str(number)]:
        if digit not in unique_digits:
            unique_digits.append(digit)
        if digit < previous_digit:
            return False
        previous_digit = digit

    if len(unique_digits) == 6:
        return False

    return True

def first_task(): 
    number_of_passwords = 0
    for i in range(108457, 562041+1):
        if check_combination(i):
            number_of_passwords += 1

    print(number_of_passwords)
