import requests
from haversine import haversine

from config import api_key, home

LOC_HOME = [float(x) for x in home.split(",")]


def get_loc_weather(loc):
    degree_sign = "\N{DEGREE SIGN}"
    condition_url = f"https://api.aerisapi.com/observations/{loc}?&format=json&filter=allstations&limit=1&{api_key}"
    resp = requests.get(condition_url).json()
    observation = resp["response"]["ob"]
    condition = observation["weatherShort"]
    temp_cel = str(observation["tempC"]) + degree_sign + "C"
    humidity = str(observation["humidity"]) + " %"
    wind_spe = str(observation["windKPH"]) + " kmph"
    wind_dir = str(observation["windDirDEG"]) + degree_sign
    full_location = str(resp["response"]["place"]["name"]).capitalize()
    print(
        "The current conditions in {0} are:\n"
        "Temeprature: {1}\n"
        "Condition  : {2}\n"
        "Humidity   : {3}\n"
        "Wind Speed : {4}\n"
        "Wind Dir.  : {5}\n".format(
            full_location, temp_cel, condition, humidity, wind_spe, wind_dir
        )
    )


def get_weather(loc):
    co_ors = []
    index = 1
    lookup_url = f"https://api.aerisapi.com/places/search?query=name:{loc}&limit=10&{api_key}"
    geolookup = requests.get(lookup_url)
    places = geolookup.json()["response"]
    if not places:
        print("Location lookup failed")
        return
    for place in places:
        coor = [place["loc"]["lat"], place["loc"]["long"]]
        co_ors.append(coor)
        how_far = round(haversine(coor, LOC_HOME), ndigits=2)
        city = place["place"]["name"]
        country = place["place"]["countryFull"]
        print(index, city, "({})".format(country), how_far, "km")
        index += 1
    choice = int(input("Enter location: "))
    get_loc_weather(co_ors[choice - 1])


def conditions():
    selection = input("Enter City Name:")
    if selection.lower() == "h":
        get_loc_weather(home)
    else:
        get_weather(selection)


if __name__ == "__main__":
    conditions()
