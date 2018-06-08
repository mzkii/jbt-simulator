# -*- coding: utf-8 -*-
import itertools
import math
import re
import time
import pygame
import sys

from Chart import Chart
from gevent import os
from pygame.locals import *

from CoordinateTimeTuple import CoordinateTimeTuple
from Difficulty import Difficulty
from Note import Note


def split_image(image):
    imageList = []
    for i in range(0, 800, 160):
        for j in range(0, 800, 160):
            surface = pygame.Surface((160, 160))
            surface.set_colorkey(000000)
            surface.blit(image, (0, 0), (j, i, j + 160, i + 160))
            imageList.append(surface)
    return imageList


def main():
    pygame.init()
    pygame.mixer.quit()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
    screen = pygame.display.set_mode((640 + 32 * 5, 640 + 32 * 5))
    pygame.display.set_caption("jbt-simulator")
    raw_maker = pygame.image.load(os.path.join('img', 'knit.png'))
    raw_maker.set_colorkey((255, 255, 255))
    maker = split_image(raw_maker)
    bg = pygame.transform.rotozoom(pygame.image.load(os.path.join('img', 'ble.png')), 0.0, 800 / 950)

    handclaps = [pygame.mixer.Sound("handclap.wav"),
                 pygame.mixer.Sound("handclap.wav"),
                 pygame.mixer.Sound("handclap.wav"),
                 pygame.mixer.Sound("handclap.wav"),
                 pygame.mixer.Sound("handclap.wav"),
                 pygame.mixer.Sound("handclap.wav"),
                 pygame.mixer.Sound("handclap.wav"),
                 pygame.mixer.Sound("handclap.wav"),
                 pygame.mixer.Sound("handclap.wav"),
                 pygame.mixer.Sound("handclap.wav")]

    handclap_index = 0
    measures = load('fumen/sample.jbt')

    for i, measure in enumerate(measures):
        notes = ''
        for note in measure:
            notes += note.to_string() + ', '
        print(i, notes)

    times = []
    for measure in measures:
        for note in measure:
            times.append(note.t)

    print(times)
    index = 0

    pygame.mixer.music.load("True Blue.mp3")
    pygame.mixer.music.play(-1)

    while True:
        screen.fill((32, 32, 32))
        screen.blit(bg, (0, 0))
        if pygame.mixer.music.get_pos() >= times[index]:
            handclaps[handclap_index].play()
            handclap_index = (handclap_index + 1) % len(handclaps)
            index = index + 1

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


## 1譜面 measures を返す
def load(path):
    position_dict = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚㉛㉜㉝㉞㉟㊱㊲㊳㊴㊵㊶㊷㊸㊹㊺㊻㊼㊽㊾㊿口'
    arrow_dict = '∧Ｖ＜＞'
    time_dict = '|－'
    dicts = position_dict + arrow_dict + time_dict

    file = open(path, 'r')
    lines = [line for line in [re.sub('[^%s]' % dicts, '', line) for line in file.readlines()] if len(line) > 0]
    tuples = [CoordinateTimeTuple(line[:4], re.sub('[%s]' % '|', '', line[4:])) for line in lines]

    times = []
    coordinates = []
    measures = []

    for tuple in tuples:
        coordinates.append(tuple.coordinate)
        if len(tuple.time) > 0:
            times.append(tuple.time)

        # 4拍( = 一小節) 貯まったら次の小節にチェンジ．
        if len(times) >= 4 and len(''.join(coordinates)) % 16 == 0:
            coordinate = ''.join(times).replace('－', '')
            time_dict = ''.join(coordinates).replace('口', '')
            diff = coordinate.translate(str.maketrans('', '', time_dict))
            if len(diff) <= 0:
                measures.append([''.join(list(coordinates)), list(times)])
                del times[:]
                del coordinates[:]

    total_time = 400
    bpm = 164
    for i, measure in enumerate(measures):
        notes = []
        coordinate = measure[0]
        times = measure[1]
        for time in times:
            for c in time:
                split_size = len(time)
                total_time += int(math.floor(60000.0 / bpm / split_size))  # 1note ごとに 1ms 程度ずれる
                if c == '－':
                    continue
                notes.append(Note(c, total_time, [], bpm))
        measures[i] = list(notes)

    return measures


if __name__ == "__main__":
    start = time.time()
    main()
    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
'''
    notes = [Note('①', 250, 1, 160), Note('②', 500, 2, 160), Note('③', 750, 3, 160)]
    measures = [Measure(1, notes), Measure(2, notes), Measure(3, notes)]
    charts = [
        Chart(Difficulty.BASIC, 3, measures),
        Chart(Difficulty.ADVANCED, 7, measures),
        Chart(Difficulty.EXTREME, 9, measures)]
    music = Music("hogehoge", "fugafuga", charts)
    music.print()
'''
