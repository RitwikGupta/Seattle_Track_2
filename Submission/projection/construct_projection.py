"""
Author: Lena Pons
Date: 2018-09-23
Project: HackTheMachine Track 2

"""

from projection import Curve, Status
from geographiclib.geodesic import Geodesic
from math import radians, cos, sin, asin, sqrt, atan2, degrees
geod = Geodesic.WGS84
EARTH_RADIUS_KM = 6378.1


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def compute_bearing(status1, status2):
    """
    compute bearing from two points
    :param status1: Status for the first time point in sequence
    :param status2: Status for the second time point in sequence
    :return: bearing in degrees
    """
    inv = geod.Inverse(status1.lat, status1.lon, status2.lat, status2.lon)
    return inv['azi2']


from math import radians, cos, sin, asin, sqrt, atan2, degrees
def predict_position(status, tdelta):
    """
    predict the next position assuming no change in heading or bearing
    :param status:
    :param tdelta:
    :return:
    """
    # initialize return value with unchanged values
    RET = Status(heading=status.heading,
                 bearing=status.bearing,
                 mmsi=status.mmsi,
                 sog=status.sog,
                 t=status.t + tdelta,
                 activity=status.activity)

    distance = status.sog * (tdelta / 60)

    lat1 = radians(status.lat)
    lon1 = radians(status.lon)
    brng = radians(status.bearing)

    lat2 = asin(sin(lat1) * cos(distance / EARTH_RADIUS_KM) +
                     cos(lat1) * sin(distance / EARTH_RADIUS_KM) * cos(brng))

    lon2 = lon1 + atan2(sin(brng) * sin(distance / EARTH_RADIUS_KM) * cos(lat1),
                             cos(distance / EARTH_RADIUS_KM) - sin(lat1) * sin(lat2))

    lat2 = degrees(lat2)
    lon2 = degrees(lon2)

    RET.lat=lat2
    RET.lon=lon2

    return RET



