class Note(object):
    def __init__(self, note, t, position, bpm):
        self.note = note
        self.t = t
        self.position = position
        self.bpm = bpm

    def to_string(self):
        return "Note[%s, %.4f, %02d, %.4f]" % (self.note, self.t, self.position, self.bpm)

    def print(self):
        print(self.to_string())
