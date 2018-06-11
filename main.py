# -*- coding: utf-8 -*-
import math
import sys

import numpy as np
import pygame
from utils import processing_measure
from gevent import os
from pygame.locals import *
from utils.chart_analyzer import load


@processing_measure.measure
def split_image(image):
    imageList = []
    for i in range(0, 800, 160):
        for j in range(0, 800, 160):
            surface = pygame.Surface((160, 160), SRCALPHA)
            surface.blit(image, (0, 0), (j, i, j + 160, i + 160))
            surface.set_colorkey((0, 0, 0), RLEACCEL)
            imageList.append(surface)
    return imageList


@processing_measure.measure
def get_nearest_value(list, num):
    """
    概要: リストからある値に最も近い値を返却する関数
    @param list: データ配列
    @param num: 対象値
    @return 対象値に最も近い値
    """
    idx = np.abs(np.asarray(list) - num).argmin()
    return list[idx]


def get_marker_frames(notes, music_pos):
    """
    概要: music_pos を基準に，パネル座標とマーカーフレームとのセットの配列を返す．
    @param notes: ノーツデータの配列
    @param music_pos: 現在再生中の楽曲再生位置
    @return パネル座標とマーカーフレームとのセットの配列
            [([13], 24), ([6], 20), ([3, 12], 16), ([16], 8), ([15], 6), ([14], 3)]
    """
    MARKER_TIME_PER_FRAME = 36
    MARKER_FRAME = 25
    MARKER_TOTAL_TIME = MARKER_TIME_PER_FRAME * MARKER_FRAME

    within_notes = [(note.positions, int(math.floor((music_pos - note.t) / MARKER_TIME_PER_FRAME)))
                    for note in [note for note in notes if music_pos - MARKER_TOTAL_TIME < note.t <= music_pos]]

    return list(within_notes)


@processing_measure.measure
def play(music, fumen):
    screen = pygame.display.get_surface()
    pygame.display.set_caption("jbt-simulator")
    clock = pygame.time.Clock()
    front_mask = pygame.image.load(os.path.join('img', 'front.png'))
    maker_frames = split_image(pygame.image.load(os.path.join('img', 'ripples.png')).convert_alpha())
    background = pygame.transform.rotozoom(pygame.image.load(os.path.join('img', 'ble.png')), 0.0, 800 / 950)
    handclap = pygame.mixer.Sound('soundeffects/handclap.wav')
    font = pygame.font.Font(None, 32)
    notes = load(fumen)

    PANEL_POSITIONS = [(y, x) for x in range(32, 640, 160 + 32) for y in range(32, 640, 160 + 32)]

    TRACK_END = USEREVENT + 1
    pygame.mixer.music.set_endevent(TRACK_END)
    pygame.mixer.music.load(music)
    pygame.mixer.music.play()

    while True:
        clock.tick(60)
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))

        for (positions, frame) in get_marker_frames(notes, pygame.mixer.music.get_pos()):
            for position in positions:
                screen.blit(maker_frames[frame], PANEL_POSITIONS[position - 1])

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == TRACK_END:
                pygame.mixer.music.stop()
                pygame.mixer.music.play()

        screen.blit(front_mask, (0, 0))
        screen.blit(font.render('%.1f' % clock.get_fps(), True, (255, 255, 255)), (36, 36))
        pygame.display.update()


@processing_measure.measure
def pygame_init():
    pygame.display.set_mode((640 + 32 * 5, 640 + 32 * 5))
    pygame.display.set_caption("jbt-simulator")
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
    pygame.font.init()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        pygame_init()
        play(sys.argv[1], sys.argv[2])
    else:
        print('Invalid argument error!!')
