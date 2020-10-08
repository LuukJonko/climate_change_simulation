from program.models.Earth import Earth
from program.models.Albedo import Albedo
from program.models.Country import Country
from program.models.Time import Time
from program.data.data import Data

from program.mapping.mapping import Mapping
from program.mapping.logging import Logging

from pathlib import Path

from sys import exit

BASEPATH = Path(__file__).parent.absolute()

try:
    logging = Logging(BASEPATH)
except ImportError:
    exit("Could not import correctly")

try:
    logging.log_event('Starting the setup', 'main')

    data_instance = Data(BASEPATH, logging)

    data = {'time': Time(),
            'albedo': Albedo(BASEPATH),
            'countries': [Country(c, data_instance.get_data(c)) for c in data_instance.get_country_names()]
            }

    earth = Earth(data)

    variable_names = {
        'earth': list(earth.__dict__.keys()),
    }

    mapping = Mapping(BASEPATH, logging, variable_names)

except Exception as E:
    logging.log_error(E, 'main')


def handler():
    for i in range(10):
        mapping.values[i] = vars(earth)
    mapping.save_csv()


def main():
    handler()


if __name__ == '__main__':
    main()
