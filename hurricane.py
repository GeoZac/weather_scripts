from datetime import datetime as dt
from math import atan2, cos, degrees, radians, sin

from haversine import haversine
from requests import get

from config import api_key, home

URL = f"https://api.aerisapi.com/tropicalcyclones/?&filter=all&limit=5&format=json&{api_key}"

LOC_HOME = [float(x) for x in home.split(",")]


def fetch_data():  # Get the current data from weather channel
    data = get(URL).json()
    return data


def deg_to_pinwheel(degree):
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    index = round(degree / (360. / len(dirs)))
    return dirs[index % len(dirs)]


def calculate_compass_bearing(point_a, point_b):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :param point_a: The tuple representing the latitude/longitude for the first point. Latitude and longitude must be in
     decimal degrees
    :param point_b: The tuple representing the latitude/longitude for the second point. Latitude and longitude must be
    in decimal degrees
    :return: The bearing in pin wheel directions
    """
    lat1 = radians(point_a[0])
    lat2 = radians(point_b[0])

    diff_long = radians(point_b[1] - point_a[1])

    x_dir = sin(diff_long) * cos(lat2)
    y_dir = cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(diff_long))

    initial_bearing = atan2(x_dir, y_dir)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    compass_bearing = round(compass_bearing, ndigits=1)
    compass_bearing = deg_to_pinwheel(compass_bearing)
    return compass_bearing


def extendedprediction(who, forecast, initial):
    for index in forecast:
        pos = index["location"]["coordinates"]
        time = dt.fromtimestamp(index["timestamp"]).strftime("%H:%M %d/%m")
        dist = round(haversine(reversed(pos), LOC_HOME), ndigits=3)
        speed = index["details"]["windSpeedKPH"]
        bearing = calculate_compass_bearing(initial, pos)
        print(f"{who} will be at {pos} on {time} which is {dist} km far with speeds of {speed} kmph moving {bearing}")
        initial = pos


def get_data(data, index):  # Fetches current state of cyclone whose name is passed as argument
    name = data[index]["profile"]["name"]
    loc = data[index]["position"]["location"]["coordinates"]
    how_far = round(haversine(reversed(loc), LOC_HOME), ndigits=3)
    wind_speed = data[index]["position"]["details"]["windSpeedKPH"]
    gust_speed = data[index]["position"]["details"]["gustSpeedKPH"]
    direction = data[index]["position"]["details"]["movement"]["direction"]
    speed = data[index]["position"]["details"]["movement"]["speedKPH"]
    movement = f"{direction} at {speed} kmph"
    print(f"{name}is at {loc} which is {how_far} km far and with winds blowing at {wind_speed} and gusts at "
          f"{gust_speed} & moving {movement}")
    minfo = input("Would you like some extended predictions ?")
    if minfo.lower() == "y":
        extendedprediction(name, data[index]["forecast"], loc)


def get_current():  # Fetches current Tropical Cyclones,to get the name to be passed in case of get_data()
    data = fetch_data()
    current = data["response"]
    index = 1
    if not current:
        print("No active cyclones tracked")
    else:
        for item in current:
            name = item["profile"]["name"]
            coor = item["position"]["location"]["coordinates"]
            how_far = round(haversine(reversed(coor), LOC_HOME), ndigits=2)
            print(index, name, how_far, "km")
            index += 1
        selection = int(input("Enter no of hurricane to track: "))
        get_data(current, selection - 1)


if __name__ == "__main__":
    get_current()
