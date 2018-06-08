# -*- coding: utf-8 -*-
import itertools
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
    screen = pygame.display.set_mode((640 + 32 * 5, 640 + 32 * 5))
    pygame.display.set_caption("jbt-simulator")
    raw_maker = pygame.image.load(os.path.join('img', 'knit.png'))
    raw_maker.set_colorkey((255, 255, 255))
    maker = split_image(raw_maker)
    bg = pygame.transform.rotozoom(pygame.image.load(os.path.join('img', 'ble.png')), 0.0, 800 / 950)
    time = pygame.time.get_ticks()

    while True:
        screen.fill((32, 32, 32))
        screen.blit(bg, (0, 0))

        for i in range(32, 640, 160 + 32):
            for j in range(32, 640, 160 + 32):
                screen.blit(maker[int((pygame.time.get_ticks() - time) / 40) % 25], (j, i))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


## 1譜面 charts型を返す
'''
Measure(1, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
Measure(2, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
Measure(3, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)

... 以下続く

'''


def load(path):
    position_dict = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚㉛㉜㉝㉞㉟㊱㊲㊳㊴㊵㊶㊷㊸㊹㊺㊻㊼㊽㊾㊿口'
    arrow_dict = '∧Ｖ＜＞'
    time_dict = '|ー'
    dicts = position_dict + arrow_dict + time_dict
    file = open(path, 'r')

    measures = itertools.zip_longest(
        *[iter([line for line in [re.sub('[^%s]' % dicts, '', line)
                                  for line in file.readlines()] if len(line) > 0])] * 4)

    measures = itertools.zip_longest(
        *[iter([[CoordinateTimeTuple(line[:4], re.sub('[%s]' % '|', '', line[4:])) for line in measure]
                for measure in measures])] * 4)

    ## tuple; 座標と時間をセットで表現している

    for measure in measures:
        for tuples in measure:
            notes = []

            # coordinate = maker座標からノーツを生成
            for button_index, coordinate in enumerate(''.join([tuple.coordinate for tuple in tuples])):
                if coordinate in '口':
                    continue
                flag = False

                #  TODO coordinate の場合でも，ノーツが重複している時がある．⑥⑥のところ．
                '''
                15
                ⑥⑥⑧口 |①ー②ー|
                口⑧口⑧ |③④⑤ー|
                ②③⑧④ |⑥ー⑦ー|
                ①⑤⑦⑦ |⑧ー⑨⑩|
                '''
                for i, note in enumerate(notes):
                    if note.note == coordinate:
                        note.position = i + 1
                        notes[i] = note
                        flag = True
                if flag:
                    continue
                if coordinate in [note.note for note in notes]:  # time で既に note が追加されていた場合
                    note = notes[notes.index(coordinate)]
                    note.position = button_index + 1
                    notes[notes.index(coordinate)] = note
                    continue
                if coordinate in '∧Ｖ＜＞':  # TODO: ホールド対応
                    continue
                notes.append(Note(coordinate, None, button_index + 1, 0))  # position(i + 1) は分かっているが，time(t) は None．

            # time = maker時間からノーツを生成
            for times in [tuple.time for tuple in tuples]:
                for time in times:
                    if time in 'ー':
                        continue
                    flag = False
                    for i, note in enumerate(notes):
                        if note.note == time:
                            note.t = 123
                            notes[i] = note
                            flag = True
                    if flag:
                        continue
                    notes.append(Note(time, 123, None, 0))  # time(t) は分かっているが，position(i + 1) は None．

            for note in notes:
                print(note.to_string(), end=', ')
            print()


if __name__ == "__main__":
    ## main()
    start = time.time()
    load('fumen/sample.jbt')
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
