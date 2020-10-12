# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 16:51:20 2020

@author: james
"""
import pygame
import math
import numpy as np
from Car2 import sprite

pygame.init()

display_width = 1280
display_height = 720

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('collision test')
clock = pygame.time.Clock()

def game_loop():
    car = sprite("player", "redsquare.png", 10, 640, 400, 5, 5, 30, 30, True, 0.2, 0.995)
    enemy2 = sprite("neutral", "redsquare.png", 5, 1000, 650, 1, 1, 30,30,True, 0, 0)

    pygame.key.set_repeat(1,1)
    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if (pygame.key.get_pressed()[pygame.K_ESCAPE]):
                gameExit = True
            car.spritecontrol()
        """
        dirx, diry = enemy.distanceto(enemy2)
        enemy.ax = -dirx * 0.025
        enemy.ay = -diry * 0.025

        dirx, diry = enemy2.distanceto(enemy)
        enemy2.ax = -dirx * 0.025
        enemy2.ay = -diry * 0.025
        """
        enemy2.spritecontrol(None, [car], [])

        car.move(display_width, display_height)
        enemy2.move(display_width, display_height)

        gameDisplay.fill(white)
        car.draw(gameDisplay)
        enemy2.draw(gameDisplay)
        pygame.display.update()
        clock.tick(144)

if __name__ == "__main__":
    game_loop()

pygame.quit()