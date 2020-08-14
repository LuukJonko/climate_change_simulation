class Country:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.sine_function = {}
        self.current_ghg_emission = 0
        self.current_co2_emission = 0
        self.current_temp = 0
        self.average_yearly_temp = 0

        self.location = data['location']
        if self.location:
            self.longitude = self.location[0]
            self.latitude = self.location[1]
