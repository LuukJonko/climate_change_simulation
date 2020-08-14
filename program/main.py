from program.models.Earth import Earth
from program.models.Albedo import Albedo
from program.models.Country import Country
from program.data.main import Data

from program.mapping.main import Mapping

from pathlib import Path

BASEPATH = Path(__file__).parent.absolute()

data_instance = Data(BASEPATH)

data = {'albedo': Albedo(), 'countries': [Country(c, data_instance.get_data(c))
                                          for c in data_instance.get_country_names()]}
earth = Earth(data)

earth_variables = list(earth.__dict__.keys())



def main():
    pass


if __name__ == '__main__':
    main()
