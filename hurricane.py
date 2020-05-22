import sys
from requests import get
from config import api_key, home
from haversine import haversine

url = "https://api.aerisapi.com/tropicalcyclones/?&filter=all&limit=5&format=json&{}".format(api_key)

home = home.split(",")
loc_home = float(home[0]), float(home[1])


def fetch_data():  # Get the current data from weather channel
    resp = get(url)
    data = resp.json()
    return data


# def fetch_hurricane(name):  # Fetch only the one passed as query
#     data = fetch_data()
#     hurricanes = data['currenthurricane']
#     for i in range(0, len(hurricanes)):
#         if hurricanes[i]['stormInfo']['stormName'] == name:
#             hurricane = hurricanes[i]
#             return hurricane
#
#
# def extendedprediction(who, forecast):
#     for index in forecast:
#         pos = index['lat'], index['lon']
#         time = index['Time']['pretty']
#         dist = round(haversine(pos, loc_home), ndigits=3)
#         speed = index['WindSpeed']['Kph']
#         print("{} will be at {} on {} which is {} km far with speeds of {} kmph".format(who, pos, time, dist, speed))
#
#
def get_data(data, index):  # Fetches current state of cyclone whose name is passed as argument
    try:
        name = data[index]["profile"]["name"]
        loc = data[index]["position"]["location"]["coordinates"]
        how_far = round(haversine(reversed(loc), loc_home), ndigits=3)
        wind_speed = data[index]["position"]["details"]["windSpeedKPH"]
        gust_speed = data[index]["position"]["details"]["gustSpeedKPH"]
        direction = data[index]["position"]["details"]["movement"]["direction"]
        speed = data[index]["position"]["details"]["movement"]["speedKPH"]
        movement = "{0} at {1} kmph".format(direction, speed)
        print(name, "is at", loc, " which is", how_far, "km far and with winds blowing at", wind_speed, "and gusts at",
              gust_speed, " & moving ", movement)
#         minfo = input("Would yo like some extended predictions ?")
#         if minfo is ('y' or 'Y'):
#             extendedprediction(name, hurricane['forecast'])
    except TypeError:
        print("{} is not a currently active Cyclone".format(index))
        print("Currently active ones are:")
        get_current()


def get_current():  # Fetches current Tropical Cyclones,to get the name to be passed in case of get_data()
    data = fetch_data()
    current = data["response"]
    index = 1
    if not current:
        print("No Active cyclones tracked")
    else:
        for item in current:
            name = item["profile"]["name"]
            coor = item["position"]["location"]["coordinates"]
            how_far = round(haversine(reversed(coor), loc_home), ndigits=2)
            print(index, name, how_far, "km")
        selection = int(input("Enter no of hurricane to track: "))
        get_data(current, selection - 1)


if __name__ == "__main__":
    get_current()
