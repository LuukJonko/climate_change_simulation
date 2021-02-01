from csv import writer, QUOTE_MINIMAL
from os.path import join as path_join
import cartopy.crs as ccrs

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
from json import load as json_load

START_YEAR = 2020


class Mapping:
    def __init__(self, BASEPATH, time_interval, logging=None, file_save_directory=None):
        self.BASEPATH = BASEPATH  # The absolute path to the parent directory of main.py
        self.logging = logging

        self.time_interval = time_interval
        print(f"Success: { self.time_interval }")

        self.values = {}  # {time { time: year,days, general_temperature, coordinates:[36 * [18 * [ temp, albedo, climate ], ...], ...]}}
        if file_save_directory:
            self.file_save_directory = file_save_directory
        else:
            self.file_save_directory = self.BASEPATH

    def save(self):
        #self.map_contour_map()
        self.save_csv()
        self.create_graphs()

    def save_csv(self):
        with open(path_join(self.file_save_directory, f'gen_temp.csv'), 'w', newline='') as csv_file:
            csv_writer = writer(csv_file, delimiter=' ',
                                quotechar='|', quoting=QUOTE_MINIMAL)
            for row in self.values.values():
                csv_writer.writerow([2020 + row['time'], row['temp']])

        with open(path_join(self.file_save_directory, f'row_temp.csv'), 'w', newline='') as csv_file:
            csv_writer = writer(csv_file, delimiter=' ',
                                quotechar='|', quoting=QUOTE_MINIMAL)
            row = list(self.values.values())[0]['coordinates'][18]
            for y_coordinate, value in enumerate(row):
                csv_writer.writerow([value[0]])

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

    def create_graphs(self):
        with open(path_join(self.BASEPATH, 'input/mapping_settings.json')) as json_file:
            settings = json_load(json_file)
            if settings['general_settings']['dark_theme']:
                plt.style.use('dark_background')
            for subject, setting in settings['graph_settings'].items():
                data = np.array([row[subject] for row in self.values.values()])
                x = np.array([row['time'] for row in self.values.values()])
                fig = plt.figure()
                for index, time in enumerate(x):
                    if time >= START_YEAR:
                        poly_x = x[index:]
                        poly_y = data[index:]
                        break
                if setting['trend']:
                    f = np.poly1d(np.polyfit(x, data, 1))
                    plt.plot(x, data, color='blue', label=setting['legend_label'])
                    plt.plot(x, f(x), color='red', linestyle='dashed', label='Trend')
                    plt.legend(loc=setting['legend_loc'], frameon=False)
                else:
                    plt.plot(x, data, color='blue')
                plt.title(setting['title'])
                plt.xlabel(setting['xlabel'])
                plt.ylabel(setting['ylabel'])
                plt.axis([START_YEAR, x[-1], min(poly_y) * .99, max(poly_y) * 1.01])
                plt.savefig(path_join(self.BASEPATH, f'output/graphs/{ subject }.png'))
                plt.close(fig)

    @staticmethod
    def get_average(li):
        return sum(li) / len(li)
