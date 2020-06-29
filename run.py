if __name__ == '__main__':
    from program import world

from geopy.geocoders import Nominatim
with Nominatim(user_agent="specify_your_app_name_here") as geolocator:
    location = geolocator.geocode("175 5th Avenue NYC")
    print(location.address)