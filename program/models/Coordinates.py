from geopy.geocoders import Nominatim


class Coordinates(object):
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.temperature = 0
        self.ghg = 0
        self.albedo = 0
        self.country = self.get_country_with_coordinates()

    def get_country_with_coordinates(self):
        async with Nominatim(user_agent='climate_change_simulator') as geolocator:
            return geolocator.geocode(f'{ 180 - self.coordinates[0] }, { 90 - self.coordinates[1] }').country()
