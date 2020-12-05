class Albedo(object):
    def __init__(self):
        self.no_sky_albedo = 0
        self.sky_albedo = .15
        self.albedo = self.no_sky_albedo + self.sky_albedo

    def calculate_albedo(self, local_climate):
        average_albedo_earth = {
            'o': .07,
            'e': .7,
            'b': .3,
            'a': .15,
            'c': .15,
            'd': .5,
        }

        if local_climate[0] in average_albedo_earth.keys():
            return average_albedo_earth[local_climate[0]] + self.sky_albedo
        else:
            return 0

    def update(self, climate):
        print(climate)
        self.no_sky_albedo = self.calculate_albedo(climate)
        print(self.no_sky_albedo)
