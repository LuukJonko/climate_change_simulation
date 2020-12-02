from geopy.geocoders import Nominatim
from math import cos, radians
import requests
import pandas as pd


class Coordinates(object):
    def __init__(self, coordinates, interval, area, data):
        self.countries = None
        self.coordinates = coordinates
        self.r_coordinates = (coordinates[0] - 180, coordinates[1] - 90)
        self.interval = interval
        self.angle = cos(coordinates[1])
        self.area = area  # (height, width)
        # self.altitude = self.get_altitude_with_coordinates()
        self.temperature = None
        self.ghg = data['ghg']
        self.albedo = data['albedo']
        self.get_country_with_coordinates(data['country_names'],  # {'country': [long, lat]}
                                          data['country_instances'])
        self.solar_constant = 1_361_000  # Watt per square meter in vacuum
        self.EnergyIn = self.solar_constant * cos(radians(coordinates[1] + self.angle)) * area[0] * area[1]
        self.temperature = (self.EnergyIn / (5.670373 * 10 ** -8 * self.area[0] * self.area[1])) ** 0.25 - 273.15

    def get_country_with_coordinates(self, names, instances):
        country_list = []
        x_reach, y_reach = 360 / self.interval, 180 / self.interval
        for country in names.items():  # ('country': [long, lat])
            if self.r_coordinates[0] + x_reach > country[1][0] > self.r_coordinates[0]:
                if self.r_coordinates[1] + y_reach > country[1][1] > self.r_coordinates[1]:
                    for c in instances:
                        if c.name == country[0]:
                            country_list.append(c)
                            print(f"Added {c.name}. { self.coordinates[0] / self.interval }, { self.coordinates[1] / self.interval }")
        print(country_list)
        self.countries = country_list
        self.ghg = sum([float(country.ghg) for country in self.countries])

    def get_altitude_with_coordinates(self):
        query = ('https://api.open-elevation.com/api/v1/lookup'
                 f'?locations={self.coordinates[0]}{self.coordinates[1]}')
        r = requests.get(query).json()  # Creates a json object
        return pd.json_normalize(r, 'results')['elevation'].values[0]  # Use pandas to
        # get the elevation out of the json object

    def update(self):
        #self.albedo = self.albedo.calculate_albedo()
        self.ghg = sum([float(country.ghg) for country in self.countries])

        self.temperature = (self.EnergyIn / (5.670373 * 10 ** -8 * self.area)) ** 0.25 - 273.15
