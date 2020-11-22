class Albedo(object):
    def __init__(self, BASEPATH):
        self.BASEPATH = BASEPATH

        self._no_sky_albedo = 0
        self._total_sky_albedo = 0

    @staticmethod
    def get_albedo_level(density, local_climate):
        average_albedo_earth = {
            'ice': .8 + .15 * density,
            'snow': .4 + .3 * density,
            'clouds': .4 + .5 * density,
            'dirt': .5 + .25 * density,
            'sand': .3 + .2 * density,
            'taiga': .15 + .2 * density,
            'planes': .25 + .5 * density,
            'forest': .1 + .1 * density,
            'water': .5 + .17 * density,
        }

        if local_climate in average_albedo_earth.keys():
            return average_albedo_earth[local_climate]
        else:
            return None 

    def calculate_albedo(self):
        return [self.get_albedo_level(coords[1]/90, data['climate']) for coords, data in self.landscape.items()]
