import sys
from requests import get
from config import api_key, home
from haversine import haversine

url = "http://api.wunderground.com/api/{}/currenthurricane/view.json".format(api_key)

home = home.split(",")
loc_home = float(home[0]), float(home[1])

def fetch_data():  # Get the current data from weather channel
    resp = get(url)
    data = resp.json()
    return data


def fetch_hurricane(name):  # Fetch only the one passed as query
    data = fetch_data()
    hurricanes = data['currenthurricane']
    for i in range(0, len(hurricanes)):
        if hurricanes[i]['stormInfo']['stormName'] == name:
            hurricane = hurricanes[i]
            return hurricane


def get_data(query):  # Fetches current state of cyclone whose name is passed as argument
    try:
        hurricane = fetch_hurricane(query)
        name = hurricane['stormInfo']['stormName']
        loc = hurricane['Current']['lat'], hurricane['Current']['lon']
        how_far = round(haversine(loc, loc_home), ndigits=3)
        wind_speed = hurricane['Current']['WindSpeed']['Kph']
        gust_speed = hurricane['Current']['WindGust']['Kph']
        direction = hurricane['Current']['Movement']['Text']
        speed = hurricane['Current']['Fspeed']['Kph']
        movement = "{0} at {1} kmph".format(direction, speed)
        print(name, "is at", loc," which is", how_far,"km far and with winds blowing at", wind_speed, "and gusts at ", gust_speed, "moving ", movement)
    except TypeError:
        print("{} is not a currently active Cyclone".format(query))
        print("Currently active ones are:")
        get_current()


def get_current():  # Fetches current Tropical Cyclones,to get the name to be passed in case of get_data()
    data = fetch_data()
    ch_list = []
    try:
        hurricanes = data['currenthurricane']
    except KeyError:
        hurricanes = []
        exit("No Active cyclones tracked")
    i = 0
    for i in range(0, len(hurricanes)):
        name = hurricanes[i]['stormInfo']['stormName']
        loc = hurricanes[i]['Current']['lat'], hurricanes[i]['Current']['lon']
        how_far = round(haversine(loc, loc_home), ndigits=2)
        ch_list.append(name)
        print(i+1, name, how_far, "km")
    ch = int(input("Enter no of hurricane to track: "))
    if ch < i+2:
        get_data(str(ch_list[ch-1]))
    else:
        exit(0)


# def pprint(name, loc, how_far, wind_speed, movement):


if __name__ == '__main__':
    try:
        get_data(sys.argv[1])
    except IndexError:
        get_current()
