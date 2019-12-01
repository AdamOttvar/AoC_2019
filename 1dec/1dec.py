import math

sum_of_fuel = 0
sum_of_fuel_for_fuel = 0

def calculate_fuel(mass):
    fuel = math.floor(mass/3) - 2
    return fuel

def recursive_fuel(mass):
	unit_fuel = calculate_fuel(mass)
	if unit_fuel <= 0:
		return 0
	else:
		return unit_fuel + recursive_fuel(unit_fuel)

with open('1dec_input.txt') as input_file:
    for line in input_file:
        mass = int(line)
        unit_fuel = calculate_fuel(mass)
        sum_of_fuel += unit_fuel
        sum_of_fuel_for_fuel += recursive_fuel(unit_fuel)
        
print("Part 1:")
print(sum_of_fuel)
print("Part 2:")
print(sum_of_fuel + sum_of_fuel_for_fuel)

