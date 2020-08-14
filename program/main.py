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

mapping = Mapping(variable_names)



def main():
    pass


if __name__ == '__main__':
    main()
