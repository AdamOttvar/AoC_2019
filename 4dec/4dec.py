#!python3

def check_combination(number):
    unique_digits = []
    repeated_digits = {}
    previous_digit = 0
    repeated_digit_counter = 0
    for digit in [int(d) for d in str(number)]:
        if digit in repeated_digits:
            repeated_digits[digit] = repeated_digits[digit] + 1
        if digit not in unique_digits:
            unique_digits.append(digit)
            repeated_digits[digit] = 1
        if digit < previous_digit:
            return False
        previous_digit = digit

    if len(unique_digits) == 6:
        return False

    one_double_digit = False
    for digit in repeated_digits:
        if repeated_digits[digit] == 2:
            one_double_digit =  True

    return one_double_digit


number_of_passwords = 0
for i in range(108457, 562041+1):
    if check_combination(i):
        number_of_passwords += 1

print(number_of_passwords)
