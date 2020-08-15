from program.models.Earth import Earth
from program.models.Albedo import Albedo
from program.models.Country import Country
from program.data.data import Data

from program.mapping.mapping import Mapping

from pathlib import Path

BASEPATH = Path(__file__).parent.absolute()

data_instance = Data(BASEPATH)

data = {'albedo': Albedo(), 'countries': [Country(c, data_instance.get_data(c))
                                          for c in data_instance.get_country_names()]}
earth = Earth(data)

variable_names = {
    'earth': list(earth.__dict__.keys()),
                  }

mapping = Mapping(BASEPATH, variable_names)


def handler():
    for i in range(1):
        mapping.values[i] = get_values()
    mapping.save_csv()


def get_values():
    values = {}
    for model in variable_names:
        values[model] = [eval(f'{ model }.{ variable_name }') for variable_name in variable_names[model]]
    return values


def main():
    handler()


if __name__ == '__main__':
    main()
