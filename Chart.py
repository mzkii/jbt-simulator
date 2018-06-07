class Chart(object):
    def __init__(self, difficulty, level, measures):
        self.difficulty = difficulty
        self.level = level
        self.measures = measures

    def to_string(self):
        measure_str = ""
        for measure in self.measures:
            measure_str += measure.to_string() + "\n"
        return "Chart[%s, %s, \n%s]" % (self.difficulty, self.level, measure_str)

    def print(self):
        print(self.to_string())
