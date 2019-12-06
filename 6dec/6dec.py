#!python3

def count_orbits(obj, objects):
    if objects[obj] == 'COM':
        return 1
    else:
        return 1 + count_orbits(objects[obj], objects)

objects = {}
with open('input6.txt') as input_file:
    for line in input_file:
        center, obj = line.strip().split(')')
        objects[obj] = center

total_orbits = 0
for obj in objects:
    orbits = count_orbits(obj, objects)
    total_orbits += orbits


print("Number of total orbits: {}".format(total_orbits))
