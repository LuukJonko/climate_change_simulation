from csv import DictWriter
from os.path import join as path_join


class Mapping:
    def __init__(self, BASEPATH, logging, variable_names, file_save_directory=None):
        self.BASEPATH = BASEPATH  # The absolute path to the parent directory of main.py
        self.logging = logging

        self.variable_names = variable_names  # Dictionary  {'model': [variable_names]}

        self.values = {}  # { time: { model: { var : value }}}
        if file_save_directory:
            self.file_save_directory = file_save_directory
        else:
            self.file_save_directory = self.BASEPATH

    def save_csv(self):
        for model in self.variable_names:
            with open(path_join(self.file_save_directory, f'{ model }.csv'), 'w', newline='') as csv_file:
                csv_writer = DictWriter(csv_file, [])
                csv_writer.writerow(self.variable_names[model])
                for time in self.values.values():
                    csv_writer.writerow(time[model])
