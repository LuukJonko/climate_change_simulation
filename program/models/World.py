from math import pi, cos


class World(object):
    def __init__(self, data, wsd):
        """
        Creates a world with a average temperature. Local temperatures are found in coordinates.
        :data = a dictionary with all the necessary instances.
        :wsd (World Specific Data) = a dictionary containing the radius and power.
        """

        self.time = data['time']
        self.albedo = data['albedo']
        self.countries = data['countries']
        self.coordinates = data['coordinates']
        self.angle = 0.39795 * cos(0.98563 * (self.time.total_days - 173))
        self.radius = wsd['radius']  # In metres
        self.surface = pi * self.radius**2
        self.globe = 4 * pi * self.radius**2
        self.PowerIn = wsd['wattPerSquareMetre'] * self.surface
        self.EnergyIn = self.PowerIn - self.PowerIn * self.albedo.albedo
        self.temperature = (self.EnergyIn / (4 * 5.670373 * 10 ** -8 * self.globe)) ** 0.25 - 273.15  # Temp in Celsius

    @staticmethod
    def get_average(li):
        return sum(li) / len(li)

    def update(self):
        print('updating...')
        self.angle = 0.39795 * cos(0.98563 * (self.time.total_days - 173))

        temp, albedo, ghg = [], [], []

        for x in self.coordinates:
            for y in x:
                y.update()
                temp.append(y.temperature)
                albedo.append(y.gen_albedo)
                ghg.append(y.ghg)
        self.temperature = self.get_average(temp)
        self.albedo.albedo = self.get_average(albedo)


