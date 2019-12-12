#!python3
import math

def apply_gravity(moons):
    for i in range(0, len(moons)):
        ego_moon = moons[i]
        for j in range(0, len(moons)):
            other_moon = moons[j]
            if i == j:
                continue
            for pos in range(0,3):    
                if ego_moon[pos] < other_moon[pos]:
                    ego_moon[pos+3] += 1
                elif ego_moon[pos] > other_moon[pos]:
                    ego_moon[pos+3] -= 1

def apply_velocity(moons):
    for i in range(0, len(moons)):
        ego_moon = moons[i]
        for pos in range(0,3):    
            ego_moon[pos] = ego_moon[pos] + ego_moon[pos+3]

def calculate_energy(moons):
    total_energy = 0
    for i in range(0, len(moons)):
        ego_moon = moons[i]
        pot_energy = abs(ego_moon[0]) + abs(ego_moon[1]) + abs(ego_moon[2])
        kin_energy = abs(ego_moon[3]) + abs(ego_moon[4]) + abs(ego_moon[5])
        total_energy += pot_energy * kin_energy
    return total_energy

def check_moons(init, current):
    same = False
    for i in range(0, len(init)):
        if init[i][:3] == current[i][:3]:
            same = True
        elif init[i][3:6] == current[i][3:6]:
            same = True
        elif init[i][6:9] == current[i][6:9]:
            same = True
    return same

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


def first_task():
    moons = []
    with open('input12.txt') as input_file:
        for line in input_file:
            for var in line.strip('<>\n').split(','):
                exec(var.strip(), globals())
            moons.append([x, y, z, 0, 0, 0])

    for step in range(0,1000):
        apply_gravity(moons)
        apply_velocity(moons)
        energy = calculate_energy(moons)
    print(moons)
    print(energy)

def second_task():
    init_moons = []
    moons = []
    with open('input12.txt') as input_file:
        for line in input_file:
            for var in line.strip('<>\n').split(','):
                exec(var.strip(), globals())
            init_moons.append([x, y, z, 0, 0, 0])
            moons.append([x, y, z, 0, 0, 0])

    axis_cycles = [0, 0, 0]
    all_same_state = False
    iteration = 1
    while not all_same_state:
        apply_gravity(moons)
        apply_velocity(moons)
        iteration += 1
        for i in range(0,len(axis_cycles)):
            if init_moons[0][i] == moons[0][i] and \
               init_moons[1][i] == moons[1][i] and \
               init_moons[2][i] == moons[2][i] and \
               init_moons[3][i] == moons[3][i]:
                if axis_cycles[i] == 0:
                    axis_cycles[i] = iteration

        all_same_state = True
        if 0 in axis_cycles:
                all_same_state = False

    print(axis_cycles)
    print(lcm(lcm(axis_cycles[0],axis_cycles[1]),axis_cycles[2]))


second_task()
