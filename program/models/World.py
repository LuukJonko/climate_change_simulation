from math import pi


class World(object):
    def __init__(self, data, wsd):
        """
        Creates a world with a average temperature. Local temperatures are found in coordinates.
        :data = a dictionary with all the necessary instances.
        :wsd (World Specific Data) = a dictionary containing the radius and power.
        """
        self.data = data
        self.time = self.data['time']
        self.albedo = self.data['albedo']
        self.countries = self.data['countries']
        self.coordinates = self.data['coordinates']
        self.time.bind_to(self.update)
        self.radius = wsd['radius']  # In metres
        self.surface = pi * self.radius**2
        self.globe = 4 * pi * self.radius**2
        self.PowerIn = wsd['wattPerSquareMetre'] * self.surface
        self.EnergyIn = self.PowerIn - self.PowerIn * self.albedo.albedo
        self.temperature = (self.EnergyIn / (5.670373 * 10 ** -8 * self.globe)) ** 0.25 - 273.15  # Temperature in Celsius

    def update(self):
        self.albedo = self.get_average(self.coordinates.albedo)
        self.EnergyIn = self.PowerIn - self.PowerIn * self.albedo
        self.temperature = (self.EnergyIn / (
                    5.670373 * 10 ** -8 * self.globe)) ** 0.25 - 273.15  # Temperature in Celsius

    def get_average(self, var):
        return sum(var) / len(self.coordinates) 
