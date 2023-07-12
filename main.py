import time

import pygame
from random import choice

pygame.init()

screen = pygame.display.set_mode((1000, 750))


def set_board():
    array = [[0] * 150 for _ in range(200)]
    for i in range(200):
        array[i][0] = 1
        array[i][-1] = 1

    for j in range(150):
        array[0][j] = 1
        array[-1][j] = 1

    return array


grid = set_board()

tile_type = 1
do_physics = False
drops = []


class Drop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.times_side = 0
        self.physics = True


def show_grid():
    screen.fill((255, 255, 255))

    for row in range(200):
        for col in range(150):
            if grid[row][col] == 1:
                pygame.draw.rect(screen, (0, 0, 0), (row * 5, col * 5, 5, 5))

    for drop in drops:
        pygame.draw.rect(screen, (0, 0, 255), (drop.x * 5, drop.y * 5, 5, 5))


def go_side(drop, side, xory, force):
    if xory == "y":
        if grid[drop.x][drop.y + side] == 0 and drop.y < 148 or force:
            drop.times_side = 0
            grid[drop.x][drop.y] = 0
            drop.y += side
            grid[drop.x][drop.y] = 2
            return True
        else:
            return False
    if xory == "x":
        if grid[drop.x + side][drop.y] == 0 and 0 < drop.x + side < 199 or force:
            drop.times_side += 1
            grid[drop.x][drop.y] = 0
            drop.x += side
            grid[drop.x][drop.y] = 2
            return True
        else:
            return False


def water_physics():
    for drop in drops:
        if drop.physics:
            sides = [-1, 1]
            if not go_side(drop, 1, "y", False):
                drop.times_side += 1
                side = choice(sides)
                if not go_side(drop, side, "x", False):
                    sides.remove(side)
                    side = sides[0]
                    if not go_side(drop, side, "x", False):
                        drop.times_side -= 1
        else:
            if go_side(drop, 1, "y", False):
                drop.physics = True

        if drop.times_side > 200:
            drop.physics = False

    time.sleep(.005)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    if do_physics:
        water_physics()

    show_grid()
    mousePos = pygame.mouse.get_pos()
    mouseClick = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        tile_type = 1
    if keys[pygame.K_2]:
        tile_type = 2

    if keys[pygame.K_SPACE]:
        do_physics = True

    if keys[pygame.K_r]:
        grid = set_board()
        do_physics = False
        drops = []

    if keys[pygame.K_d]:
        do_physics = False
        drops = []
        for i in range(200):
            for j in range(150):
                if grid[i][j] == 2:
                    grid[i][j] = 0

    try:
        if mouseClick[0]:
            if tile_type == 2:
                for i in range(2):
                    for j in range(2):
                        if grid[mousePos[0] // 5 + i][mousePos[1] // 5 + j] != 2:
                            drops.append(Drop(mousePos[0] // 5 + i, mousePos[1] // 5 + j))
                            grid[mousePos[0] // 5 + i][mousePos[1] // 5 + j] = 2
            else:
                for i in range(2):
                    for j in range(2):
                        grid[mousePos[0] // 5 + i][mousePos[1] // 5 + j] = 1

        if mouseClick[2]:
            for i in range(2):
                for j in range(2):
                    grid[mousePos[0] // 5 + i][mousePos[1] // 5 + j] = 0

    except IndexError:
        pass

    pygame.display.update()
