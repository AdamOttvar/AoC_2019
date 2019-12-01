import math

sum_of_fuel = 0
sum_of_fuel_for_fuel = 0

def calculate_fuel(mass):
    fuel = math.floor(mass/3) - 2
    return fuel

with open('1dec_input.txt') as input_file:
    for line in input_file:
        mass = int(line)
        unit_fuel = calculate_fuel(mass)
        sum_of_fuel += unit_fuel
        while unit_fuel > 0:
            unit_fuel = calculate_fuel(unit_fuel)
            sum_of_fuel_for_fuel += unit_fuel if unit_fuel > 0 else 0       

print("Part 1:")
print(sum_of_fuel)
print("Part 2:")
print(sum_of_fuel + sum_of_fuel_for_fuel)

