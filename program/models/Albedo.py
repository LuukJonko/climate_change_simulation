from random import random


class Albedo(object):
    def __init__(self, climate = None):
        self.albedo = 0

        self.average_albedo_earth = {
            'o': .07,
            'e': .65,
            'b': .3,
            'a': .15,
            'c': .15,
            'd': .5,
        }

        self.chance_for_cloud = {
            'o': .7,
            'e': 0,
            'b': 0,
            'a': 0,
            'c': 0,
            'd': 0,
        }

        self.local_climate = climate

    def calculate_albedo(self):
        if self.local_climate[0] in self.average_albedo_earth.keys():
            return self.average_albedo_earth[self.local_climate[0]]
        else:
            return 0

    def random_cloud_generator(self, temperature):
        chance = (temperature * 3) / 100 * self.average_albedo_earth[self.local_climate[0]]
        return random() < chance

    def snow_fall(self, temperature):
        return self.random_cloud_generator(temperature) and temperature >= 0

    def update(self, temperature):
        self.albedo = .7 if self.random_cloud_generator(temperature) == True else 0
        self.albedo = self.average_albedo_earth['e'] if self.snow_fall(temperature) == True \
            else self.calculate_albedo()
