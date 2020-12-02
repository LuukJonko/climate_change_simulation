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
        self.time.bind_to(self.update)
        self.angle = 0.39795 * cos(0.98563 * (self.time._total - 173))
        self.radius = wsd['radius']  # In metres
        self.surface = pi * self.radius**2
        self.globe = 4 * pi * self.radius**2
        self.PowerIn = wsd['wattPerSquareMetre'] * self.surface
        self.EnergyIn = self.PowerIn - self.PowerIn * self.albedo.albedo
        self.temperature = (self.EnergyIn / (5.670373 * 10 ** -8 * self.globe)) ** 0.25 - 273.15  # Temp in Celsius

    def update(self):
        self.angle = 0.39795 * cos(0.98563 * (self.time._total - 173))

        self.albedo = self.get_average(self.coordinates.albedo)
        self.EnergyIn = self.PowerIn - self.PowerIn * self.albedo
        self.temperature = (self.EnergyIn / (
                    5.670373 * 10 ** -8 * self.globe)) ** 0.25 - 273.15  # Temperature in Celsius

    def get_average(self, var):
        return sum(var) / len(self.coordinates) 
