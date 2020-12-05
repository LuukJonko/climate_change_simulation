try:
    from models.World import World
    from models.Albedo import Albedo
    from models.GHG import GHG
    from models.Country import Country
    from models.Coordinates import Coordinates
    from models.Time import Time
    from data.data import Data

    from mapping.mapping import Mapping
    from mapping.logging import Logging

except ModuleNotFoundError:
    from program.models.World import World
    from program.models.Albedo import Albedo
    from program.models.GHG import GHG
    from program.models.Country import Country
    from program.models.Coordinates import Coordinates
    from program.models.Time import Time
    from program.data.data import Data

    from program.mapping.mapping import Mapping
    from program.mapping.logging import Logging

from pathlib import Path

from sys import stdout
from os import getpid
from psutil import Process

BASEPATH = Path(__file__).parent.absolute()

logging = Logging(BASEPATH)  # Create an instance of the logging
data_instance = Data(BASEPATH, logging)


def create_list_coordinates(interval, instances):
    x_interval, y_interval = int(360 / interval), int(180 / interval)
    coordinates_list = []
    for x in range(x_interval):
        new_list = []
        for y in range(y_interval):
            new_list.append(Coordinates(coords := (x * interval, y * interval), interval, (1731000 / 36, 1731000 / 18),
                                        data_instance.get_climate_with_coordinates(coords, (interval, interval)),
                                        instances))
           # stdout.write(f"\rCreated coordinate ({x},{y}). {x_interval * y_interval}")
           # stdout.flush()
        coordinates_list.append(new_list)
    #stdout.write('\n')
    return coordinates_list


def save_values(t, world, mapping):
    coordinates_list = []
    for x in world.coordinates:
        new_list = []
        for y in x:
            new_list.append([y.temperature, y.albedo.albedo, y.climate])
        coordinates_list.append(new_list)
    mapping.values[t] = {
        'time': world.time.time,
        'temp': world.temperature,
        'coordinates': coordinates_list,
    }


def setup(coordinates_interval):
    logging.log_event('Starting the setup', 'main')  # Log the start up to the loggin file

    wsd = {'radius': 6371000, 'wattPerSquareMetre': 1368}

    country_list = [Country(c, GHG, data_instance.get_data(c)) for c in data_instance.get_country_names()]

    data = dict(time=Time(), albedo=Albedo(),
                countries=country_list,
                coordinates=create_list_coordinates(coordinates_interval, {
                    'albedo': Albedo,
                    'ghg': GHG,
                    'country_names': data_instance.get_country_with_location(),  # {'country': [long, lat], ...}
                    'country_instances': country_list,
                }))

    earth = World(data, wsd)

    for c_x in earth.coordinates:
        for c_y in c_x:
            c_y.world_instance = earth

    mapping = Mapping(BASEPATH)

    return earth, data['time'], mapping


def handler(length, earth, time, mapping):
    for t in range(length):
        time.proceed()
        earth.update()
        save_values(t, earth, mapping)
    mapping.save_csv()


def display_current_memory_usage():
    process = Process(getpid())
    return process.memory_info().rss / 1024 / 1024


def main():
    earth, time, mapping = setup(10)
    handler(10, earth, time, mapping)
    return earth, mapping


if __name__ == '__main__':
    main()
