from math import pi


class Earth(object):
    def __init__(self, data):
        self.time = 0
        self.data = data
        self.albedo = self.data['albedo']
        self.countries = self.data['countries']
        self.albedo.bind_to(self.update)
        self.Energie = 0  # In Joule
        self.radius = 6371000  # In metres
        self.surface = pi * self.radius**2
        self.globe = 4 * pi * self.radius**2
        self.PowerIn = 1368 * self.surface
        self.EnergieIn = self.PowerIn - self.PowerIn * self.albedo.albedo
        self.temperature = (self.EnergieIn / (5.670373*10**-8 * self.globe))**0.25 - 273.15  # Temperature in Celsius

    def update(self, albedo):
        self.EnergieIn = self.PowerIn - self.PowerIn * albedo
        self.temperature = (self.EnergieIn / (
                    5.670373 * 10 ** -8 * self.globe)) ** 0.25 - 273.15  # Temperature in Celsius


