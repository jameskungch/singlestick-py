# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 01:49:51 2020

@author: james
"""
import pygame
import math

pygame.init()

display_width = 1600
display_height = 1000

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('wut r u doing')
clock = pygame.time.Clock()

def draw(spritetodraw):
    gameDisplay.blit(spritetodraw.img, (spritetodraw.x, spritetodraw.y))

def distanceto(spritea, spriteb):
    xdiff = spritea.x - spriteb.x
    ydiff = spritea.y - spriteb.y
    magnitude = math.sqrt(xdiff * xdiff + ydiff * ydiff)
    xnorm = xdiff / magnitude
    ynorm = ydiff / magnitude
    return xnorm, ynorm

class sprite():
    def __init__(self, image, x=0, y=0, vx_max=20, vy_max=20, img_width=0, img_height=0, bounce = True, accel = 0.2, drag = 0):
        self.img = pygame.image.load(image)
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.vx_max = vx_max
        self.vy_max = vy_max
        self.img_width = img_width
        self.img_height = img_height
        self.bounce = bounce
        self.accel = accel
        self.drag = drag
    # def draw(self):
    #     gameDisplay.blit(self.img,(self.x,self.y))
    def move(self, display_width, display_height):
        # if self.drag != 0:
        #     self.ax *= self.drag
        #     self.ay *= self.drag
            #magnitude = math.sqrt(self.ax * self.ax + self.ay * self.ay)
        self.vx += self.ax
        if self.vx > self.vx_max:
            self.vx = self.vx_max
        if self.vx < -self.vx_max:
            self.vx = -self.vx_max
        self.vy += self.ay
        if self.vy > self.vy_max:
            self.vy = self.vy_max
        if self.vy < -self.vy_max:
            self.vy = -self.vy_max
        if self.drag != 0:
            self.vx *= self.drag
            self.vy *= self.drag
        self.x += self.vx
        self.y += self.vy
        if self.bounce:
            if self.x >= display_width - self.img_width:
                self.vx = -self.vx
            if self.x < 0:
                self.vx = -self.vx
            if self.y > display_height - self.img_height:
                self.vy = -self.vy
            if self.y < 0:
                self.vy = -self.vy
        else:
            if self.x > display_width - self.img_width:
                self.x = 0
            if self.x < 0:
                self.x = display_width - self.img_width
            if self.y > display_height - self.img_height:
                self.y = 0
            if self.y < 0:
                self.y = display_height - self.img_height


def game_loop():
    car = sprite("racecar.png", 800, 800, 20, 20, 73, 82, True, 0.2, 0.995)
    ball = sprite("target.png", 800, 500, 20, 20, 50, 50, True, 0, 0.99)
    pygame.key.set_repeat(1,1)

    gameExit = False
    # spacedown = False
    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    car.ax = -car.accel
                if event.key == pygame.K_RIGHT:
                    car.ax = car.accel
                if event.key == pygame.K_UP:
                    car.ay = -car.accel
                if event.key == pygame.K_DOWN:
                    car.ay = car.accel
                if event.key == pygame.K_SPACE:
                    dirx, diry = distanceto(car, ball)
                    ball.ax = dirx
                    ball.ay = diry
                if event.key == pygame.K_ESCAPE:
                    gameExit = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    car.ax = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    car.ay = 0
                if event.key == pygame.K_SPACE:
                    ball.ax = 0
                    ball.ay = 0

        car.move(display_width, display_height)
        ball.move(display_width, display_height)
        gameDisplay.fill(white)
        draw(car)
        draw(ball)

        # if x > display_width - car_width or x < 0:
        #     gameExit = True



        pygame.display.update()
        clock.tick(144)



game_loop()
pygame.quit()
# quit()