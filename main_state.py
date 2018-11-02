import random
import json
import os

from pico2d import *

import game_framework
import title_state
import pause_state


name = "MainState"

image = None
tile1 = None
tile2 = None
tile3 = None
tile4 = [None, None, None, None, None, None]
tile1_up = None
tile1_left = None
tile1_down = None

boy = None
monster1 = None
pauses = None
font = None



class Boy:
    def __init__(self):
        self.x, self.y = 600, 720-64
        self.image = load_image('character_right_stand0.png')
        self.image1 = load_image('character_right_stand1.png')
        self.move_left = 0
        self.move_right = 0
        self.move_up = 0
        self.move_down = 0
        self.count = 0

    def update(self):
        if self.move_left == 1:
            self.x -= 2
        if self.move_right == 1:
            self.x += 2
        if self.move_up == 1:
            self.y += 2
        if self.move_down == 1:
            self.y -= 2

        self.count = (self.count + 1) % 120

    def draw(self):
        if self.count < 110:
            self.image.draw(self.x, self.y)
        else:
            self.image1.draw(self.x, self.y)


class Monster1:
    def __init__(self):
        self.x, self.y = 0, 720-320
        self.image = load_image('monster1.png')
        self.move = 1

    def update(self):
        if self.move == 1 and self.x >= 576:
            self.move = 2
        elif self.move == 2 and self.y <= 720 - 576:
            self.move = 3

        if self.move == 1:
            self.x += 1.5
        elif self.move == 2:
            self.y -= 1.5
        elif self.move == 3:
            self.x += 1.5

    def draw(self):
            self.image.draw(self.x, self.y)


def enter():
    global boy, monster1
    boy = Boy()
    monster1 = Monster1()

    global image, tile1, tile2, tile3, tile1_up, tile1_left, tile1_down, tile4
    image = load_image('tower1.png')
    tile1 = load_image("tile5.png")
    tile2 = load_image('tile2.png')
    tile3 = load_image('tile3.png')
    tile1_up = load_image('tile1_up.png')
    tile1_left = load_image('tile1_left.png')
    tile1_down = load_image('tile1_down.png')
    tile4[0] = load_image('tile4_high.png')
    tile4[1] = load_image('tile4_LD.png')
    tile4[2] = load_image('tile4_LU.png')
    tile4[3] = load_image('tile4_RD.png')
    tile4[4] = load_image('tile4_RU.png')
    tile4[5] = load_image('tile4_width.png')


def exit():
    global boy, monster1
    del (boy)
    del (monster1)

    global image, tile1, tile2, tile3, tile1_up, tile1_left, tile1_down, tile4
    del (image)
    del (tile1)
    del (tile2)
    del (tile3)
    del (tile1_up)
    del (tile1_left)
    del (tile1_down)
    del (tile4)


def pause():
    pass

def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.push_state(pause_state)

        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            boy.move_left = 1
        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
            boy.move_left = 0

        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            boy.move_right = 1
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            boy.move_right = 0

        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            boy.move_up = 1
        elif event.type == SDL_KEYUP and event.key == SDLK_UP:
            boy.move_up = 0

        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            boy.move_down = 1
        elif event.type == SDL_KEYUP and event.key == SDLK_DOWN:
            boy.move_down = 0


def update():
    boy.update()
    monster1.update()


def draw():
    clear_canvas()

    image.draw(640, 360)

    for i in range(60):
        if game_framework.text2[i] == '1':
            tile1.draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)
        elif game_framework.text2[i] == '2':
            tile2.draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)
        elif game_framework.text2[i] == '3':
            tile3.draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)
        elif game_framework.text2[i] == '4':
            tile4[0].draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)
        elif game_framework.text2[i] == '5':
            tile4[1].draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)
        elif game_framework.text2[i] == '6':
            tile4[2].draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)
        elif game_framework.text2[i] == '7':
            tile4[3].draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)
        elif game_framework.text2[i] == '8':
            tile4[4].draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)
        elif game_framework.text2[i] == '9':
            tile4[5].draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)

    for i in range(60):
        if game_framework.text3[i] == '1':
            tile1_up.draw((i % 10) * 128 + 128, 720 - (i // 10) * 128)
        elif game_framework.text3[i] == '2':
            tile1_left.draw((i % 10) * 128 + 160, 720 - (i // 10) * 128 - 32)
        elif game_framework.text3[i] == '3':
            tile1_down.draw((i % 10) * 128 + 96, 720 - (i // 10) * 128 + 32)
        elif game_framework.text3[i] == '4':
            tile1_left.draw((i % 10) * 128 + 160, 720 - (i // 10) * 128 - 32)
            tile1_down.draw((i % 10) * 128 + 96, 720 - (i // 10) * 128 + 32)

    monster1.draw()
    boy.draw()

    update_canvas()