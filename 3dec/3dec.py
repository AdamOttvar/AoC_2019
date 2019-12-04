#!python3
class Wiring:
    def __init__(self):
        self.schematic = {}
        self.lengths = {}
        self.min_distance = 999999999
        self.wire_counter = 0

    def read_input(self, file):
        with open(file) as input_file:
            wire_paths = input_file.read().strip().split()

        for index in range(len(wire_paths)):
            wire_paths[index] = [self.split_instruction(instruction) for instruction in wire_paths[index].split(',')]

        self.wire_instructions = wire_paths

    def split_instruction(self, instruction):
        head = instruction.rstrip('0123456789')
        tail = instruction[len(head):]
        return head, int(tail)

    def visit_coord(self, coordinate, wire_nbr):
        if str(coordinate) in self.schematic:
            if self.schematic[str(coordinate)] == wire_nbr:
                self.schematic[str(coordinate)] = wire_nbr
                return False
            elif self.schematic[str(coordinate)] == 99:
                return True
            else:
                self.schematic[str(coordinate)] = 99
                distance = abs(coordinate[0])+abs(coordinate[1])
                self.min_distance = distance if distance < self.min_distance else self.min_distance
                return False
        else:
            self.schematic[str(coordinate)] = wire_nbr
            return False

    def run_one_instruction(self, instr, curr_coord, wire_nbr):
        direction = instr[0]
        steps = instr[1]
        if direction == "U":
            for i in range(curr_coord[1]+1, curr_coord[1]+1+steps):
                self.wire_counter += 1
                curr_coord = [curr_coord[0], i]
                intersect = self.visit_coord(curr_coord, wire_nbr)
                if intersect:
                    if wire_nbr == 1:
                        self.lengths[str(curr_coord)] = [self.wire_counter, 0]
                    else:
                        self.lengths[str(curr_coord)][1] = self.wire_counter

        elif direction == "D":
            for i in range(curr_coord[1]-1, curr_coord[1]-1-steps, -1):
                self.wire_counter += 1
                curr_coord = [curr_coord[0], i]
                intersect = self.visit_coord(curr_coord, wire_nbr)
                if intersect:
                    if wire_nbr == 1:
                        self.lengths[str(curr_coord)] = [self.wire_counter, 0]
                    else:
                        self.lengths[str(curr_coord)][1] = self.wire_counter

        elif direction == "R":
            for i in range(curr_coord[0]+1, curr_coord[0]+1+steps):
                self.wire_counter += 1
                curr_coord = [i, curr_coord[1]]
                intersect = self.visit_coord(curr_coord, wire_nbr)
                if intersect:
                    if wire_nbr == 1:
                        self.lengths[str(curr_coord)] = [self.wire_counter, 0]
                    else:
                        self.lengths[str(curr_coord)][1] = self.wire_counter

        elif direction == "L":
            for i in range(curr_coord[0]-1, curr_coord[0]-1-steps, -1):
                self.wire_counter += 1
                curr_coord = [i, curr_coord[1]]
                intersect = self.visit_coord(curr_coord, wire_nbr)
                if intersect:
                    if wire_nbr == 1:
                        self.lengths[str(curr_coord)] = [self.wire_counter, 0]
                    else:
                        self.lengths[str(curr_coord)][1] = self.wire_counter

        else:
            print("Not a correct instruction")

        return curr_coord


    def run_wire(self, wire_nbr):
        current_coordinate = [0, 0]
        instructions = self.wire_instructions[wire_nbr-1]
        self.wire_counter = 0
        for instruction in instructions:
            current_coordinate = self.run_one_instruction(instruction, current_coordinate, wire_nbr)

    def first_task(self):
        self.read_input('input3.txt')
        self.run_wire(1)
        self.run_wire(2)
        print("Smallest distance: {}".format(self.min_distance))

    def second_task(self):
        self.run_wire(1)
        self.run_wire(2)

        min_length = 99999999999
        for intersect in self.lengths:
            values = self.lengths[intersect]
            length = values[0] + values[1]
            min_length = length if length < min_length else min_length
        print("Least steps: {}".format(min_length))


wiring = Wiring()
wiring.first_task()
wiring.second_task()
