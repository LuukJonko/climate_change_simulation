import csv
import os
import pathlib
from math import pi, sin
from geopy import Nominatim

from imutils import paths

geolocator = Nominatim(user_agent='climate_change_simulation')


class Country:
    def __init__(self, name):
        self.name = name
        self.data = {}
        self.sine_function = {}
        self.current_ghg_emission = 0
        self.current_co2_emission = 0
        self.current_temp = 0
        self.average_yearly_temp = 0

        self.time = 0

        self.location = geolocator.geocode(name)
        self.longitude = self.location.longitude
        self.latitude = self.location.latitude

    def get_csv_data(self):
        for file in list(paths.list_files('./csv')):  # Make a list of all the paths in the csv directory
            with open(file, 'r') as csv_file:  # Open the files
                contents = list(csv.reader(csv_file))  # Read the contents and make a 3d list out of it
                self.data[os.path.splitext(os.path.basename(csv_file.name))[0]] = None  # Set data of to None incase nothing is found
                for country in contents:  # Go over all countries in the csv file
                    if country[0].lower() == self.name.lower():  # Check if it is the right country, otherwise continue
                        amount_with_year = {}  # Create empty dictionary
                        for index, amount in enumerate(country[1:]):  # Go over all the data for the country with index
                            amount_with_year[contents[0][index + 1]] = amount  # Link the year to the data
                        self.data[os.path.splitext(os.path.basename(csv_file.name))[0]] = amount_with_year  # Put it all in the dictionary under the name of the csv file
                        try:
                            self.average_yearly_temp = self.data['average_yearly_temperature']['current']  # Set average yearly temp as a easily accessible variable
                        except TypeError:
                            self.average_yearly_temp = None  # If there is no recorded temp then it is None
                        break

    def temperature_function(self, x):
        return self.sine_function['A'] * sin(self.sine_function['B'] * x + self.sine_function['C']) + \
               self.sine_function['D']

    def calculate_sinus_function(self):
        self.sine_function['A'] = self.current_temp / (sin(pi/6 * self.time % 12) + 9.5)
        self.sine_function['B'] = 2 * pi / 12
        self.sine_function['C'] = 0
        self.sine_function['D'] = self.average_yearly_temp


countries = []
for country in ['GLOBAL TOTAL', 'Afghanistan', 'Albania', 'Algeria', 'Angola', 'Anguilla', 'Antigua and Barbuda',
                'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain',
                'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia',
                'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'British Virgin Islands', 'Brunei', 'Bulgaria',
                'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands',
                'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Cook Islands',
                'Costa Rica', 'CÃ´te dâ€™Ivoire', 'Croatia', 'Cuba', 'CuraÃ§ao', 'Cyprus', 'Czechia',
                'Democratic Republic of the Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador',
                'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia',
                'Falkland Islands', 'Faroes', 'Fiji', 'Finland', 'France and Monaco', 'French Guiana',
                'French Polynesia', 'Gabon', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland',
                'Grenada', 'Guadeloupe', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras',
                'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'International Aviation',
                'International Shipping', 'Iran', 'Iraq', 'Ireland', 'Israel and Palestine, State of',
                'Italy, San Marino and the Holy See', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati',
                'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Lithuania',
                'Luxembourg', 'Macao', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Martinique',
                'Mauritania', 'Mauritius', 'Mexico', 'Moldova', 'Mongolia', 'Morocco', 'Mozambique', 'Myanmar/Burma',
                'Namibia', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria',
                'North Korea', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea',
                'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'RÃ©union', 'Romania',
                'Russia', 'Rwanda', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis',
                'Saint Lucia', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa',
                'SÃ£o TomÃ© and PrÃ\xadncipe', 'Saudi Arabia', 'Senegal', 'Serbia and Montenegro', 'Seychelles',
                'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa',
                'South Korea', 'Spain and Andorra', 'Sri Lanka', 'Sudan and South Sudan', 'Suriname', 'Sweden',
                'Switzerland and Liechtenstein', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'The Gambia',
                'Timor-Leste', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan',
                'Turks and Caicos Islands', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom',
                'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Western Sahara', 'Yemen',
                'Zambia', 'Zimbabwe']:
    countries.append(Country(country))

for country in countries:
    country.get_csv_data()
