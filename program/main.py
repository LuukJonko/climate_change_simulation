from program.models.Earth import Earth
from program.models.Albedo import Albedo
from program.models.Country import Country

from program.mapping.main import Mapping

from pathlib import Path

BASEPATH = Path(__file__).parent.absolute()


def main():
    data = Albedo()
    earth = Earth(data)

    earth_variables = list(earth.__dict__.keys())


def setup():
    pass


if __name__ == '__main__':
    main()
