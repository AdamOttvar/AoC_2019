#!python3

class AsteroidMap(object):
    def __init__(self):
        super(AsteroidMap, self).__init__()
        self.asteroid_coords = []
        self.asteroid_sightings = {}
        self.asteroid_nbr_of_sightings = {}
        self.vaporized_astroids = []
        self.asteroid_station = None

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
        if dx > 0 and dy < 0:
            quarter = 'RU'
        elif dx > 0 and dy > 0:
            quarter = 'RD'
        elif dx < 0 and dy > 0:
            quarter = 'LD'
        else:
            quarter = 'LU'
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
            return quarter + str(dxdy)

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

    def get_max(self):
        max_sightings = 0
        best_asteroid = None
        for asteroid, value in self.asteroid_nbr_of_sightings.items():
            if value > max_sightings:
                max_sightings = value
                best_asteroid = asteroid
        return best_asteroid, max_sightings

    def place_station(self, asteroid):
        self.asteroid_station = asteroid

    def spin_lazer_once(self):
        asteroid_sightings = self.asteroid_sightings[self.asteroid_station]
        list_of_keys = [*self.asteroid_sightings[self.asteroid_station]]
        list_of_RU_keys = [float(value[2:]) for value in list_of_keys if 'RU' in value]
        list_of_RU_keys.sort(reverse=True)
        list_of_RD_keys = [float(value[2:]) for value in list_of_keys if 'RD' in value]
        list_of_RD_keys.sort(reverse=True)
        list_of_LD_keys = [float(value[2:]) for value in list_of_keys if 'LD' in value]
        list_of_LD_keys.sort(reverse=True)
        list_of_LU_keys = [float(value[2:]) for value in list_of_keys if 'LU' in value]
        list_of_LU_keys.sort(reverse=True)
        if 'U' in asteroid_sightings:
            self.asteroid_coords.remove(asteroid_sightings['U'][0])
            self.vaporized_astroids.append(asteroid_sightings['U'][0])
        for asteroid in list_of_RU_keys:
            key = 'RU' + str(asteroid)
            self.asteroid_coords.remove(asteroid_sightings[key][0])
            self.vaporized_astroids.append(asteroid_sightings[key][0])
        if 'R' in asteroid_sightings:
            self.asteroid_coords.remove(asteroid_sightings['R'][0])
            self.vaporized_astroids.append(asteroid_sightings['R'][0])
        for asteroid in list_of_RD_keys:
            key = 'RD' + str(asteroid)
            self.asteroid_coords.remove(asteroid_sightings[key][0])
            self.vaporized_astroids.append(asteroid_sightings[key][0])
        if 'D' in asteroid_sightings:
            self.asteroid_coords.remove(asteroid_sightings['D'][0])
            self.vaporized_astroids.append(asteroid_sightings['D'][0])
        for asteroid in list_of_LD_keys:
            key = 'LD' + str(asteroid)
            self.asteroid_coords.remove(asteroid_sightings[key][0])
            self.vaporized_astroids.append(asteroid_sightings[key][0])
        if 'L' in asteroid_sightings:
            self.asteroid_coords.remove(asteroid_sightings['L'][0])
            self.vaporized_astroids.append(asteroid_sightings['L'][0])
        for asteroid in list_of_LU_keys:
            key = 'LU' + str(asteroid)
            self.asteroid_coords.remove(asteroid_sightings[key][0])
            self.vaporized_astroids.append(asteroid_sightings[key][0])


def first_task():
    asteroid_map = AsteroidMap()
    asteroid_map.read_map('input10.txt')
    asteroid_map.calculate_asteroids()
    asteroid_map.count_sightings()
    best_asteroid, max_sightings = asteroid_map.get_max()
    print("First answer: ")
    print(best_asteroid)
    print(max_sightings)

def second_task():
    asteroid_map = AsteroidMap()
    asteroid_map.read_map('input10.txt')
    asteroid_map.calculate_asteroids()
    asteroid_map.count_sightings()
    best_asteroid, max_sightings = asteroid_map.get_max()
    asteroid_map.place_station(best_asteroid)
    asteroid_map.spin_lazer_once()
    while len(asteroid_map.vaporized_astroids) < 299:
        asteroid_map.calculate_asteroids()
        asteroid_map.spin_lazer_once()

    print(asteroid_map.vaporized_astroids[199])

second_task()
