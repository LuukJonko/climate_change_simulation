from math import exp

SNOW_ALBEDO = 0.8
CLOUD_COVERAGE = 0.4

DROPLET_SIZE = 10 ** -4
SEA_DIFFERENCE = 5


class Albedo(object):
    def __init__(self, climate=None):
        self.albedo = .33
        self.ground_albedo = .12
        self.cloud_albedo = .26

        self.snow_coverage = 0

        self.average_albedo_earth = {
            'o': .07,
            'e': .20,
            'b': .10,
            'a': .10,
            'c': .10,
            'd': .10,
        }

        self.local_climate = climate

    def cloud_albedo_generator(self, temp_ground):
        water_quantity = 54 * 10 ** -3 * exp(0.05 * temp_ground)
        droplet_size = DROPLET_SIZE if self.local_climate[0] == 'o' else DROPLET_SIZE / SEA_DIFFERENCE
        return water_quantity/(water_quantity + 4.47 * 10 ** 3 * droplet_size)

    def snow_generator(self, temp_ground):
        self.snow_coverage = 1 if temp_ground <= -40 else 1 - 0.00033 * (temp_ground + 40) ** 2 \
            if -40 < temp_ground <= 15 else 0

    def calculate_albedo(self):
        if self.local_climate[0] in self.average_albedo_earth.keys():
            return self.average_albedo_earth[self.local_climate[0]]
        else:
            return 0

    def update(self, temp_ground):
        self.ground_albedo = self.calculate_albedo()
        if self.local_climate[0] != 'o':
            self.snow_generator(temp_ground)
            self.ground_albedo = (self.snow_coverage * SNOW_ALBEDO + (1 - self.snow_coverage) * self.ground_albedo + self.ground_albedo) / 2
        self.cloud_albedo = self.cloud_albedo_generator(temp_ground)
        self.albedo = 1 - ((1 - (CLOUD_COVERAGE * self.cloud_albedo)) * (1 - self.ground_albedo))
        #self.albedo = 0.4 * self.cloud_albedo + .6 * self.ground_albedo
