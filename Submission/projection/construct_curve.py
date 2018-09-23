"""
Author: Lena Pons
Date: 2018-09-23
Project: HackTheMachine Track 2

"""

from projection import Curve, Status, construct_projection
from datetime import timedelta


def _get_points_from_dataframe(df, mmsi, time):
    """
    TODO: make this actually populate the dicts
    create dicts from dataframe to pass to _construct_point
    :param df: dataframe containing AIS data
    :param mmsi: mmsi of interest
    :param time: timestamp for t0
    :return: dict containing Status information
    """
    points = list()
    idx = df.index[df['MMSI'] == mmsi & df['BaseDateTime'] == time]
    try:
        previdx = idx - 1
    except ValueError:
        prevstat = None
    try:
        postidx = idx + 1
    except ValueError:
        poststat = None



def _construct_point(point):
    """
    from a dict-like point, construct a Status object
    :param point: dict-like representation of one row of AIS data
    :return: Status object constructed from single row
    """
    p = Status()
    p.mmsi = point['MMSI']
    p.lat = point['LAT']
    p.lon = point['LON']
    p.sog = point['SOG']
    p.bearing = point['COG']
    p.heading = point['Heading']
    p.activity = point['Status']
    p.t = point['BaseDateTime']


def _compute_tdelta(points):
    """
    compute the time difference between two observed points
    :param points: list of dict-like point objects (AIS data records)
    :return: time difference in minutes
    """
    pminus1 = points[len(points)-2]
    pzero = points[len(points)-1]
    tdelta = pzero['BaseDateTime'] - pminus1['BaseDateTime']
    return tdelta / timedelta(minutes=1)


def construct_observed(points, tdelta=None):
    """
    constuct a curve from observed points
    :param points: list of dict-like ais data that feeds into _construct_point
    :param tdelta: if a tdelta is specified
    :return: a curve constructed from observed data
    """
    curve = Curve()
    # compute tdelta if not passed
    if tdelta is not None:
        curve.tdelta = tdelta
    else:
        curve.tdelta = _compute_tdelta(points)
    status_points = list()
    # construct Status objects from passed points
    for p in points:
        status_points.append(_construct_point(p))
    curve.points = status_points

    return curve


def construct_projected(points, tdelta):
    """
    construct a curve based on observed past data and a single forward projection
    NOTE: heading, bearing, SOG, activity are all carried forward from the last observed point
    :param points: list of dict-like ais data that feeds into _construct_point
    :param tdelta: the tdelta for the projection
    :return: a curve containing past data and a single projected point
    """
    curve = Curve(actual=False)
    curve.tdelta = tdelta
    status_points = list()
    # construct Status objects from passed points
    for p in points:
        status_points.append(_construct_point(p))
    last = status_points[len(status_points) - 1]
    # predict next point
    projection = construct_projection.predict_position(status_points[last])
    status_points.append(projection)
    curve.points = status_points
    return curve
