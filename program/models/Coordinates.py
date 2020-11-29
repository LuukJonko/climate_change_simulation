from geopy.geocoders import Nominatim
from math import cos, radians
import requests
import pandas as pd


class Coordinates(object):
    def __init__(self, coordinates, area, data):
        self.coordinates = coordinates
        self.r_coordinates = (coordinates[0] - 180, coordinates[1] - 90)
        self.angle = cos(coordinates[1])
        self.area = area  # (height, width)
        # self.altitude = self.get_altitude_with_coordinates()
        self.temperature = None
        self.ghg = data['ghg']
        self.albedo = data['albedo']
        # self.country = self.get_country_with_coordinates()
        self.solar_constant = 1_361_000  # Watt per square meter in vacuum

        self.EnergyIn = self.solar_constant * cos(radians(coordinates[1] + self.angle)) * area[0] * area[1]
        self.temperature = (self.EnergyIn / (5.670373 * 10 ** -8 * self.area[0] * self.area[1])) ** 0.25 - 273.15

    async def get_country_with_coordinates(self):
        async with Nominatim(user_agent='climate_change_simulator') as geolocator:
            return geolocator.geocode(f'{self.r_coordinates[0]}, {self.r_coordinates[1]}').country()

    def get_altitude_with_coordinates(self):
        query = ('https://api.open-elevation.com/api/v1/lookup'
                 f'?locations={self.coordinates[0]}{self.coordinates[1]}')
        r = requests.get(query).json()  # Creates a json object
        return pd.json_normalize(r, 'results')['elevation'].values[0]  # Use pandas to
        # get the elevation out of the json object

    def update(self):
        self.albedo = self.albedo.calculate_albedo()

        self.temperature = (self.EnergyIn / (5.670373 * 10 ** -8 * self.area)) ** 0.25 - 273.15
