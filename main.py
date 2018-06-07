# -*- coding: utf-8 -*-
import pygame
from gevent import os
from pygame.locals import *
import sys


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


if __name__ == "__main__":
    ## main()
    file = open('fumen/sample.jbt', 'r')
    string = file.readlines()
    bpm = 155
    haku = 0
    shosetsu = 0
    for i in string:
        for j in i:
            if j == '⑯':
                print(j, end="")