from program.models.Earth import Earth
from program.models.Albedo import Albedo
from program.models.Country import Country
from program.models.Coordinates import Coordinates
from program.models.Time import Time
from program.data.data import Data

from program.mapping.mapping import Mapping
from program.mapping.logging import Logging

from pathlib import Path

from sys import exit

BASEPATH = Path(__file__).parent.absolute()


def create_list_coordinates(interval):
    x_interval, y_interval = 360 / interval, 180 / interval
    coordinates_list = [[] * y_interval] * x_interval
    for x, x_value in enumerate(coordinates_list):
        for y, _ in enumerate(x_value):
            coordinates_list[x][y] = Coordinates((), 0, 0)


def setup(coordinates_interval):
    logging = Logging(BASEPATH)

    try:
        logging.log_event('Starting the setup', 'main')

        data_instance = Data(BASEPATH, logging)

        data = {'time': Time(),
                'albedo': Albedo(BASEPATH),
                'countries': [Country(c, data_instance.get_data(c)) for c in data_instance.get_country_names()],
                'coordinates': create_list_coordinates(coordinates_interval)
                }

        earth = Earth(data)

        variable_names = {
            'earth': list(earth.__dict__.keys()),
        }

        mapping = Mapping(BASEPATH, logging, variable_names)

        return earth, data['time'], mapping

    except Exception as E:
        logging.log_error(E, 'main')
        exit(1)


def handler(length, earth, time, mapping):
    for t in range(length):
        time.proceed()
        mapping.values[t] = vars(earth)
    mapping.save_csv()


def main():
    earth, time, mapping = setup(10)
    handler(10, earth, time, mapping)


if __name__ == '__main__':
    main()
