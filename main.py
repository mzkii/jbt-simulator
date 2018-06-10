# -*- coding: utf-8 -*-
import math

import numpy as np
import time
import pygame
import sys
from gevent import os
from pygame.locals import *
from ChartAnalyzer import load


def split_image(image):
    imageList = []
    for i in range(0, 800, 160):
        for j in range(0, 800, 160):
            surface = pygame.Surface((160, 160), SRCALPHA)
            surface.blit(image, (0, 0), (j, i, j + 160, i + 160))
            surface.set_colorkey((0, 0, 0), RLEACCEL)
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
    MARKER_FRAME_PER_MS = 36
    PANEL_SIZE = 16
    frames = [[] for i in range(PANEL_SIZE)]
    for note in notes:
        if music_pos - MARKER_FRAME_PER_MS * 25 < note.t <= music_pos:
            for position in note.positions:
                frame = int(math.floor((music_pos - note.t) / MARKER_FRAME_PER_MS))
                frames[position - 1].append(frame)
    return list(frames)


def play(music, fumen):
    screen = pygame.display.set_mode((640 + 32 * 5, 640 + 32 * 5))
    front_mask = pygame.image.load(os.path.join('img', 'front.png'))
    maker = pygame.image.load(os.path.join('img', 'blur.png')).convert_alpha()
    maker_frames = split_image(maker)
    background = pygame.transform.rotozoom(pygame.image.load(os.path.join('img', 'ble.png')), 0.0, 800 / 950)
    handclap = pygame.mixer.Sound("handclap.wav")

    measures = load(fumen)
    notes = []
    for measure in measures:
        for note in measure:
            notes.append(note)
            note.print()

    positions = []
    for i in range(32, 640, 160 + 32):
        for j in range(32, 640, 160 + 32):
            positions.append([j, i])

    TRACK_END = USEREVENT + 1
    pygame.mixer.music.set_endevent(TRACK_END)
    pygame.mixer.music.load(music)
    pygame.mixer.music.play()

    while True:
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))

        for i, frames in enumerate(get_marker_frames(notes, pygame.mixer.music.get_pos())):
            for frame in frames:
                p = (positions[i][0], positions[i][1])
                screen.blit(maker_frames[frame], p)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == TRACK_END:
                pygame.mixer.music.stop()
                pygame.mixer.music.play()

        screen.blit(front_mask, (0, 0))
        pygame.display.update()


def pygame_init():
    pygame.mixer.quit()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
    pygame.display.set_caption("jbt-simulator")


if __name__ == "__main__":
    start = time.time()
    pygame_init()
    play('Stand Alone Beat Masta.mp3', 'fumen/sample.jbt')
    print("elapsed_time:{0}".format(time.time() - start) + "[sec]")