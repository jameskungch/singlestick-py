# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 11:16:53 2020

@author: james
"""
import pygame
import math

pygame.init()

display_width = 1280
display_height = 720

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('wut r u doing')
clock = pygame.time.Clock()


class sprite():
    def __init__(self, spritetype, image, x=0, y=0, vx_max=20, vy_max=20,
                 img_width=0, img_height=0, bounce=True, accel=0.2, drag=0,
                 deadtimeseparation=50):
        if spritetype in ["player", "ball", "enemy"]:
            self.spritetype = spritetype
        else:
            raise ValueError("spritetype must be one of 'player', 'ball', 'enemy'!")
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
        self.deadtime = 50
        self.deadtimeseparation = deadtimeseparation

    def draw(self, gameDisplay):
        gameDisplay.blit(self.img, (self.x, self.y))

    def getv(self):
        return math.sqrt(self.vx * self.vx + self.vy * self.vy)

    def distanceto(self, target, normed=True):
        xdiff = self.x - target.x
        ydiff = self.y - target.y
        magnitude = math.sqrt(xdiff * xdiff + ydiff * ydiff)
        if normed:
            xnorm = xdiff / magnitude
            ynorm = ydiff / magnitude
            return xnorm, ynorm
        else:
            return xdiff, ydiff, magnitude

    def istouching(self, target):
        xdiff, ydiff, magnitude = self.distanceto(target, normed=False)
        if (abs(xdiff) < (self.img_width + target.img_width)/2 and
            abs(ydiff) < (self.img_height + target.img_width)/2):
            return True

    def spritecontrol(self, target=None, friendslist=[], enemieslist = []):
        if self.spritetype == "player":
            if (pygame.key.get_pressed()[pygame.K_LEFT]):
                self.ax = -self.accel
            if (pygame.key.get_pressed()[pygame.K_RIGHT]):
                self.ax = self.accel
            if (pygame.key.get_pressed()[pygame.K_UP]):
                self.ay = -self.accel
            if (pygame.key.get_pressed()[pygame.K_DOWN]):
                self.ay = self.accel
            if not(pygame.key.get_pressed()[pygame.K_LEFT] or
                   pygame.key.get_pressed()[pygame.K_RIGHT]):
                self.ax=0
            if not(pygame.key.get_pressed()[pygame.K_UP] or
                   pygame.key.get_pressed()[pygame.K_DOWN]):
                self.ay=0

        if self.spritetype == "ball":
            if target == None:
                raise ValueError("no target defined!")
            if (pygame.key.get_pressed()[pygame.K_SPACE]):
                dirx, diry = self.distanceto(target, normed = True)
                self.ax = -dirx
                self.ay = -diry
            if not(pygame.key.get_pressed()[pygame.K_SPACE]):
                self.ax =0
                self.ay = 0

        if self.spritetype == "enemy":
            dirx, diry = self.distanceto(target)
            self.ax = -dirx * 0.05
            self.ay = -diry * 0.05
            if friendslist != []:
                for i in friendslist:
                    xdiff, ydiff, magnitude = self.distanceto(i, False)
                    if magnitude < self.img_width * 2:
                        self.ax += xdiff / magnitude * 0.05
                        self.ay += ydiff / magnitude * 0.05
                        # print("triggered")
            if enemieslist != []:
                for i in enemieslist:
                    xdiff, ydiff, magnitude = self.distanceto(i, False)
                    if magnitude < self.img_width * 3 and i.getv() >= 1:
                        self.ax += xdiff / magnitude * 0.5
                        self.ay += ydiff / magnitude * 0.5
                        # print("running away")



    def move(self, display_width, display_height):
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
    car = sprite("player", "racecar.png", 640, 400, 5, 5, 73, 82, True, 0.2, 0.995)
    ball = sprite("ball", "target.png", 640, 360, 20, 20, 50, 50, True, 0, 0.99)
    enemy = sprite("enemy", "redsquare.png", 50, 50, 1, 1, 30,30,True, 0, 0)
    enemy2 = sprite("enemy", "redsquare.png", 1000, 650, 1, 1, 30,30,True, 0, 0)
    enemy3 = sprite("enemy", "redsquare.png", 1000, 50, 1, 1, 30,30,True, 0, 0)

    pygame.key.set_repeat(1,1)
    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if (pygame.key.get_pressed()[pygame.K_ESCAPE]):
                gameExit = True
            car.spritecontrol()
            ball.spritecontrol(car)

        enemy.spritecontrol(car, [enemy2, enemy3], [ball])
        enemy2.spritecontrol(car, [enemy, enemy3], [ball])
        enemy3.spritecontrol(car, [enemy, enemy2], [ball])

        car.move(display_width, display_height)
        ball.move(display_width, display_height)
        enemy.move(display_width, display_height)
        enemy2.move(display_width, display_height)
        enemy3.move(display_width, display_height)

        for j in [enemy, enemy2, enemy3]:
            if car.istouching(j):
                if car.deadtime >= car.deadtimeseparation:
                    print("dead!")
                    car.deadtime = 0
            if ball.istouching(j) and ball.getv() >= 5:
                if j.deadtime >= j.deadtimeseparation:
                    print("kill!")
                    j.deadtime = 0
            j.deadtime += 1

        car.deadtime += 1

        gameDisplay.fill(white)
        car.draw(gameDisplay)
        ball.draw(gameDisplay)
        enemy.draw(gameDisplay)
        enemy2.draw(gameDisplay)
        enemy3.draw(gameDisplay)

        pygame.display.update()
        clock.tick(144)


game_loop()
pygame.quit()
