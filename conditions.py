import requests
import sys
from config import api_key


# noinspection PyUnusedLocal
def get_weather(loc):
    lookup_url = "http://api.wunderground.com/api/{}/geolookup/q/India/".format(api_key)
    condition_url = "http://api.wunderground.com/api/{}/conditions/q/India/".format(api_key)

    degree_sign = u'\N{DEGREE SIGN}'
    geolookup = requests.get(lookup_url + loc + ".json")
    # if (len(geolookup.json())) == 2:
    try:
        resp = requests.get(condition_url + loc + ".json")
        condition = resp.json()['current_observation']['weather']
        # temp_c = str(resp.json()['current_observation']['temp_c']) + '' + degree_sign + "C"
        # temp_f = str(resp.json()['current_observation']['temp_f']) + '' + degree_sign + "F"
        # temp = temp_c + "/" +temp_f
        temp = resp.json()['current_observation']['temperature_string']
        full_location = resp.json()['current_observation']['display_location']['full']
        weather = "The current temperature in {0} is {1}. It's currently humid and partly cloudy️.".format(
            full_location, temp)
        print(weather)
    except KeyError:
        print("WeatherUndeground Sucks")




if __name__ == '__main__':
    try:
        get_weather(sys.argv[1])
    except IndexError:
        get_weather(input("Enter City Name:"))
