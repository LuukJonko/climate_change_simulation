from csv import writer, QUOTE_MINIMAL
from os.path import join as path_join


class Mapping:
    def __init__(self, BASEPATH, logging=None, file_save_directory=None):
        self.BASEPATH = BASEPATH  # The absolute path to the parent directory of main.py
        self.logging = logging

        self.values = {}  # { time, general_temperature, coordinates:[36 * [18 * [ temp, albedo, climate ], ...], ...]}
        if file_save_directory:
            self.file_save_directory = file_save_directory
        else:
            self.file_save_directory = self.BASEPATH

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

    @staticmethod
    def get_average(li):
        return sum(li) / len(li)
