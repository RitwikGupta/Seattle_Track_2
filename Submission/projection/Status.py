"""
Author: Lena Pons
Date: 2018-09-23
Project: HackTheMachine Track 2

"""


class Status():

    def __init__(self, mmsi, lat, lon, sog, bearing, heading, activity, t):
        self.mmsi = mmsi
        self.lat = lat
        self.lon = lon
        self.sog = sog
        self.bearing = bearing
        self.heading = heading
        self.activity = activity
        self.t = t