# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys


def main():
    pygame.init()  # 初期化
    screen = pygame.display.set_mode((600, 400))  # ウィンドウサイズの指定
    pygame.display.set_caption("Pygame Test")  # ウィンドウの上の方に出てくるアレの指定

    while True:
        screen.fill((255, 63, 10,))  # 背景色の指定。RGBだと思う
        pygame.display.update()  # 画面更新

        for event in pygame.event.get():  # 終了処理
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
