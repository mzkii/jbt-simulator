# -*- coding: utf-8 -*-
import math

import numpy as np
import re
import time
import pygame
import sys
from gevent import os
from pygame.locals import *
from CoordinateTimeTuple import CoordinateTimeTuple
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


def get_nearest_value(list, num):
    """
    概要: リストからある値に最も近い値を返却する関数
    @param list: データ配列
    @param num: 対象値
    @return 対象値に最も近い値
    """

    # リスト要素と対象値の差分を計算し最小値のインデックスを取得
    idx = np.abs(np.asarray(list) - num).argmin()
    return list[idx]


def get_marker_frames(notes, music_pos):
    # len(frames) = 16; [[13], [12], [10], [10, 15], [], [], [], [], [], [], [], [], [], [], [], []]
    frames = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    for note in notes:
        if music_pos - 40 * 25 <= note.t < music_pos:
            for position in note.positions:
                try:
                    frame = int(math.floor((music_pos - note.t) / 40))
                    if 0 <= frame < 25:
                        frames[position - 1].append(frame)
                    else:
                        raise ValueError("index out of range!! frame = {}".format(frame))
                except ValueError as e:
                    print(e)

    return list(frames)


def main():
    pygame.mixer.quit()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
    screen = pygame.display.set_mode((640 + 32 * 5, 640 + 32 * 5))
    pygame.display.set_caption("jbt-simulator")
    raw_maker = pygame.image.load(os.path.join('img', 'blur.png'))
    front = pygame.image.load(os.path.join('img', 'front.png'))
    raw_maker.set_colorkey((255, 255, 255))
    maker = split_image(raw_maker)
    bg = pygame.transform.rotozoom(pygame.image.load(os.path.join('img', 'ble.png')), 0.0, 800 / 950)
    handclap = pygame.mixer.Sound("handclap.wav")
    measures = load('fumen/sample.jbt')

    notes = []
    for measure in measures:
        for note in measure:
            notes.append(note)

    for note in notes:
        note.print()

    TRACK_END = USEREVENT + 1
    pygame.mixer.music.set_endevent(TRACK_END)
    pygame.mixer.music.load("Stand Alone Beat Masta.mp3")
    pygame.mixer.music.play()

    positions = []
    for i in range(32, 640, 160 + 32):
        for j in range(32, 640, 160 + 32):
            positions.append([j, i])

    while True:
        screen.fill((16, 16, 16))
        # screen.blit(bg, (0, 0))

        # print(get_marker_frames(notes, pygame.mixer.music.get_pos()))
        for i, frames in enumerate(get_marker_frames(notes, pygame.mixer.music.get_pos())):
            for frame in frames:
                p = (positions[i][0], positions[i][1])
                screen.blit(maker[frame], p)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == TRACK_END:
                pygame.mixer.music.stop()
                pygame.mixer.music.play()

        screen.blit(front, (0, 0))
        pygame.display.update()



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
        if len(times) >= 4 and len(''.join(coordinates)) % 16 == 0:
            coordinate = ''.join(times).replace('－', '')
            time_dict = ''.join(coordinates).replace('口', '')
            diff = coordinate.translate(str.maketrans('', '', time_dict))
            if len(diff) <= 0:
                measures.append([''.join(list(coordinates)), list(times)])
                del times[:]
                del coordinates[:]

    total_time = 0
    bpm = 200
    for i, measure in enumerate(measures):
        notes = []
        ## 0 ['口口④口口口口③口口②口口口口①', ['－－－－', '－－－－', '－－－－', '①②③④']]
        coordinates = measure[0]
        times = measure[1]
        for time in times:
            for c in time:
                split_size = len(time)
                total_time += 60000.0 / bpm / split_size  # 1note ごとに 1ms 程度ずれる
                if c == '－':
                    continue
                notes.append(Note(c, total_time, [], bpm))

        for j, note in enumerate(notes):
            note.positions = [(i % 16) + 1 for i, x in enumerate(coordinates) if x == note.note]
            notes[j] = note

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
