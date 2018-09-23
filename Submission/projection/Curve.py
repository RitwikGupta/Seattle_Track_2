"""
Author: Lena Pons
Date: 2018-09-23
Project: HackTheMachine Track 2

"""


class Curve():

    def __init__(self, tdelta, actual=True, points=None):
        """
        object to contain a series of points at t - 1, t0, t + 1
        :param tdelta:
        :param actual: a flag for whether t+1 point is observed (actual) or predicted.
        if actual = True, the t + 1 point is observed
        :param points: list of three Status objects for t - 1, t0 and t + 1
        """
        self.tdelta = tdelta
        self.points = points
        self.actual = actual
