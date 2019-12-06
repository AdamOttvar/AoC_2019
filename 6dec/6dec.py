#!python3

def get_first_intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2][-1]
    return lst3

def count_all_orbits(obj, target, objects):
    if objects[obj] == target:
        return 1
    else:
        return 1 + count_all_orbits(objects[obj], target, objects)

def get_all_centers(obj, target, objects, centers):
    if objects[obj] == target:
        return centers.append(target)
    else:
        get_all_centers(objects[obj], target, objects, centers)
        return centers.append(objects[obj])

def first_task(objects):
    total_orbits = 0
    for obj in objects:
        orbits = count_all_orbits(obj, 'COM', objects)
        total_orbits += orbits

    print("Number of total orbits: {}".format(total_orbits))

def second_task(objects):
    you_centers = []
    san_centers = []
    get_all_centers('YOU', 'COM', objects, you_centers)
    get_all_centers('SAN', 'COM', objects, san_centers)

    closest_center = get_first_intersection(you_centers, san_centers)

    you_nbr_orbits = count_all_orbits('YOU', closest_center, objects)
    san_nbr_orbits = count_all_orbits('SAN', closest_center, objects)

    # We do not want to go to the target, we want to get into orbit,
    # hence -2 (or -1-1)
    nbr_to_same_orbit = you_nbr_orbits + san_nbr_orbits -2

    print("Number of orbital transfers: {}".format(nbr_to_same_orbit))


objects = {}
with open('input6.txt') as input_file:
    for line in input_file:
        center, obj = line.strip().split(')')
        objects[obj] = center

first_task(objects)
second_task(objects)
