# -*- coding: utf-8 -*-


class CoordinateTimeTuple(object):
    def __init__(self, coordinate, time):
        self.coordinate = coordinate
        self.time = time

    def to_string(self):
        return "CoordinateTimeTuple[%s, %s]" % (self.coordinate, self.time)

    def print(self):
        print(self.to_string())
