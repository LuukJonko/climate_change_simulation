from csv import writer, QUOTE_MINIMAL
from os.path import join as path_join
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np


class Mapping:
    def __init__(self, BASEPATH, logging=None, file_save_directory=None):
        self.BASEPATH = BASEPATH  # The absolute path to the parent directory of main.py
        self.logging = logging

        self.values = {}  # {time { time, general_temperature, coordinates:[36 * [18 * [ temp, albedo, climate ], ...], ...]}}
        if file_save_directory:
            self.file_save_directory = file_save_directory
        else:
            self.file_save_directory = self.BASEPATH

    def save(self):
        self.map_contour_map()

    def save_csv(self):
        with open(path_join(self.file_save_directory, f'gen_temp.csv'), 'w', newline='') as csv_file:
            csv_writer = writer(csv_file, delimiter=' ',
                                quotechar='|', quoting=QUOTE_MINIMAL)
            for row in self.values.values():
                csv_writer.writerow([2020 + row['time'], row['temp']])

    def save_coordinate_csv(self):
        for model in ['temp', 'albedo']:
            with open(path_join(self.file_save_directory, f'coordinaten_{ model }.csv'), 'w', newline='') as csv_file:
                csv_writer = writer(csv_file, delimiter=' ',
                                    quotechar='|', quoting=QUOTE_MINIMAL)
                for x in self.values['coordinates']:
                    for y in x:
                        pass

    def map_contour_map(self):
        for index, model in enumerate(['temp', 'albedo']):
            for values in self.values.values():
                from cartopy.examples.waves import sample_data
                ax = plt.axes(projection=ccrs.Robinson())
                ax.set_global()
                lons, lats = sample_data(shape=(36, 18))[:2]
                data = self.make_fit([[y[index] for y in x] for x in values['coordinates']])
                plt.contourf(lons, lats, data, transform=ccrs.PlateCarree())

                ax.coastlines()
                ax.gridlines()

                plt.savefig(path_join(self.BASEPATH, f"output/images/{ model }{ values['time'] }.png"))

    @staticmethod
    def make_fit(li):
        max_value = max(map(max, li))
        min_value = min(map(min, li))
        m = max_value if max_value >= abs(min_value) else min_value
        return [[y / m for y in x] for x in li]

    @staticmethod
    def get_average(li):
        return sum(li) / len(li)

