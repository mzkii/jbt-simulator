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
            surface.blit(image, (0, 0), (j, i, j + 160, i + 160))
            imageList.append(surface)
    return imageList


def main():
    pygame.init()
    screen = pygame.display.set_mode((640 + 32 * 5, 640 + 32 * 5))
    pygame.display.set_caption("jbt-simulator")
    image = split_image(pygame.image.load(os.path.join('img', 'syoku.png')))
    index = 0

    while True:
        screen.fill((32, 32, 32))

        for i in range(32, 640, 160 + 32):
            for j in range(32, 640, 160 + 32):
                screen.blit(image[index % 25], (j, i))

        index = index + 1
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
