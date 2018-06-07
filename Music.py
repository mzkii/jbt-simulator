class Music(object):
    def __init__(self, title, artist, charts):
        self.title = title
        self.artist = artist
        self.charts = charts

    def to_string(self):
        music_str = ""
        for chart in self.charts:
            music_str += chart.to_string() + "\n--------------------------------\n"
        return "Music[%s, %s, \n%s]" % (self.title, self.artist, music_str)

    def print(self):
        print(self.to_string())
