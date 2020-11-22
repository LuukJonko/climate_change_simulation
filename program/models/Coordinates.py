from geopy.geocoders import Nominatim
from math import cos, radians


class Coordinates(object):
    def __init__(self, coordinates, area, height, data):
        self.coordinates = coordinates
        self.angle = cos(coordinates[1])
        self.area = area  # (height, width)
        self.temperature = data['temperature']
        self.ghg = data['ghg']
        self.albedo = data['albedo']
        self.country = self.get_country_with_coordinates()
        self.solar_constant = 1337  # Watt per square meter

        self.EnergyIn = self.solar_constant * cos(radians(abs(coordinates[1]))) * area[0] * area[1]
        self.temperature = (self.EnergyIn / (5.670373*10**-8 * self.area))**0.25 - 273.15

    def get_country_with_coordinates(self):
        async with Nominatim(user_agent='climate_change_simulator') as geolocator:
            return geolocator.geocode(f'{ 180 - self.coordinates[0] }, { 90 - self.coordinates[1] }').country()

    def update(self):
        self.albedo = self.albedo.calculate_albedo()

        self.temperature = (self.EnergyIn / (5.670373*10**-8 * self.area))**0.25 - 273.15
