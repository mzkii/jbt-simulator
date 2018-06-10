# -*- coding: utf-8 -*-


class Measure(object):
    def __init__(self, measure, notes):
        self.measure = measure
        self.notes = notes

    def to_string(self):
        note_str = ""
        for note in self.notes:
            note_str += note.to_string() + "\n"
        return "Measure[%d, \n%s]" % (self.measure, note_str)

    def print(self):
        print(self.to_string())
