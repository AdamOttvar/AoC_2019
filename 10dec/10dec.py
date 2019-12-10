#!python3

class AsteroidMap(object):
    def __init__(self):
        super(AsteroidMap, self).__init__()
        self.asteroid_coords = []
        self.asteroid_sightings = {}
        self.asteroid_nbr_of_sightings = {}

    def read_map(self, file):
        with open(file) as input_file:
            y_coord = 0
            for line in input_file:
                x_coord = 0
                for coord in line:
                    if '#' in coord:
                        self.asteroid_coords.append((x_coord,y_coord))
                    x_coord += 1
                y_coord += 1

    def calculate_diff(self, x0, x1, y0, y1):
        dx = x1 - x0
        dy = y1 - y0
        if dx > 0:
            half_side = 'R'
        else:
            half_side = 'L'
        if dy == 0:
            if dx < 0:
                return 'L'
            else:
                return 'R'
        elif dx == 0:
            if dy < 0:
                return 'U'
            else:
                return 'D'
        else:
            dxdy = dx/dy
            return half_side + str(dxdy)

    def calculate_distance(self, x0, x1, y0, y1):
        dx = x1 - x0
        dy = y1 - y0
        return abs(dx) + abs(dy)

    def calculate_asteroids(self):
        for ego_asteroid in self.asteroid_coords:
            self.asteroid_sightings[ego_asteroid] = {}
            for other_asteroid in self.asteroid_coords:
                if other_asteroid == ego_asteroid:
                    continue
                dxdy = self.calculate_diff(ego_asteroid[0],
                                           other_asteroid[0],
                                           ego_asteroid[1],
                                           other_asteroid[1])
                distance = self.calculate_distance(ego_asteroid[0],
                                                   other_asteroid[0],
                                                   ego_asteroid[1],
                                                   other_asteroid[1])
                if dxdy in self.asteroid_sightings[ego_asteroid]:
                    prev_distance = self.asteroid_sightings[ego_asteroid][dxdy][1]
                    if distance < prev_distance:
                        self.asteroid_sightings[ego_asteroid][dxdy] = [other_asteroid, distance]
                else:
                    self.asteroid_sightings[ego_asteroid][dxdy] = [other_asteroid, distance]

    def count_sightings(self):
        for asteroid in self.asteroid_sightings:
            self.asteroid_nbr_of_sightings[asteroid] = len(self.asteroid_sightings[asteroid])

    def print_max(self):
        max_sightings = 0
        best_asteroid = None
        for asteroid, value in self.asteroid_nbr_of_sightings.items():
            if value > max_sightings:
                max_sightings = value
                best_asteroid = asteroid
        print("Asteroid: {}, Sightings: {}".format(best_asteroid,max_sightings))

def first_task():
    asteroid_map = AsteroidMap()
    asteroid_map.read_map('input10.txt')
    asteroid_map.calculate_asteroids()
    asteroid_map.count_sightings()
    asteroid_map.print_max()

first_task()