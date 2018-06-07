# -*- coding: utf-8 -*-
import time

import pygame
from gevent import os
from pygame.locals import *
import sys
from Chart import Chart
from Difficulty import Difficulty
from Measure import Measure
from Music import Music
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


def load(path):
    file = open(path, 'r')
    dict = [
        '①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩',

        '⑪', '⑫', '⑬', '⑭', '⑮', '⑯', '⑰', '⑱', '⑲', '⑳',

        '㉑', '㉒', '㉓', '㉔', '㉕', '㉖', '㉗', '㉘', '㉙', '㉚',

        '㉛', '㉜', '㉝', '㉞', '㉟', '㊱', '㊲', '㊳', '㊴', '㊵',

        '㊶', '㊷', '㊸', '㊹', '㊺', '㊻', '㊼', '㊽', '㊾', '㊿',

        '∧', 'Ｖ', '＜', '＞', '口', '|', 'ー',
    ]
    lines = file.readlines()
    for line in lines:
        br = False
        for c in line:
            if c in dict:
                pass
                print(c, end="")
                br = True
        if br:
            print()


if __name__ == "__main__":
    ## main()
    start = time.time()
    load('fumen/sample.jbt')
    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

    '''
        dict = {
            '①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5, '⑥': 6, '⑦': 7, '⑧': 8, '⑨': 9, '⑩': 10,
    
            '⑪': 11, '⑫': 12, '⑬': 13, '⑭': 14, '⑮': 15, '⑯': 16, '⑰': 17, '⑱': 18, '⑲': 19, '⑳': 20,
    
            '㉑': 21, '㉒': 22, '㉓': 23, '㉔': 24, '㉕': 25, '㉖': 26, '㉗': 27, '㉘': 28, '㉙': 29, '㉚': 30,
    
            '㉛': 31, '㉜': 32, '㉝': 33, '㉞': 34, '㉟': 35, '㊱': 36, '㊲': 37, '㊳': 38, '㊴': 39, '㊵': 40,
    
            '㊶': 41, '㊷': 42, '㊸': 43, '㊹': 44, '㊺': 45, '㊻': 46, '㊼': 47, '㊽': 48, '㊾': 49, '㊿': 50,
    
            '∧': 51, 'Ｖ': 52, '＜': 53, '＞': 54, '口': 55, '|': 56, 'ー': 57,
        }
    '''

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
