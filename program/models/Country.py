class Country(object):
    def __init__(self, name, instances, data):
        self.name = name
        self.data = data
        self.csv_data = data['csv']  # {'subject': {'year': 'value', ...}, ...}
        self.ghg = self.csv_data['GHG_emissions']['2015\nMton CO2eq']

        self.location = data['location']  # [long, lat]
        if self.location:
            self.longitude = self.location[0]
            self.latitude = self.location[1]
