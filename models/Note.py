# -*- coding: utf-8 -*-


class Note(object):
    def __init__(self, note, t, positions, bpm):
        self.note = note
        self.t = t
        self.positions = positions
        self.bpm = bpm

    def to_string(self):
        return "Note[%s, %d, %s, %.4f]" % (self.note, int(self.t), self.positions, self.bpm)

    def print(self):
        print(self.to_string())
