import requests
import sys
from config import api_key, home


# noinspection PyUnusedLocal
def get_weather(loc):
    lookup_url = "https://api.aerisapi.com/places/search?query=name:{}&limit=10&{}".format(loc, api_key)
    condition_url = "https://api.aerisapi.com/observations/{}?&format=json&filter=allstations&limit=1&{}".format(home, api_key)

    degree_sign = u'\N{DEGREE SIGN}'
    geolookup = requests.get(lookup_url)
    # if (len(geolookup.json())) == 2:
    try:
        resp = requests.get(condition_url)
        condition = resp.json()["response"]["ob"]["weatherShort"]
        # temp_c = str(resp.json()['current_observation']['temp_c']) + '' + degree_sign + "C"
        # temp_f = str(resp.json()['current_observation']['temp_f']) + '' + degree_sign + "F"
        # temp = temp_c + "/" +temp_f
        temp = resp.json()["response"]["ob"]["tempC"]
        full_location = resp.json()["response"]["place"]["name"]
        weather = "The current temperature in {0} is {1}.".format(
            full_location, temp)
        print(weather)
    except KeyError:
        print("WeatherUndeground Sucks")




if __name__ == '__main__':
    try:
        get_weather(sys.argv[1])
    except IndexError:
        get_weather(input("Enter City Name:"))
