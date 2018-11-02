import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from tile import Tile
from monster1 import Monster1

mouse_x = 0
mouse_y = 0


name = "MainState"

boy = None
monster1 = None


class Ui:
    global mouse_x
    global mouse_y

    def __init__(self):
        self.tower1_icon = load_image('tower1_icon.png')
        self.tower1_click = load_image('tower1_click.png')
        self.select_sp = load_image('select.png')

        self.left_click = 0
        self.cho_tower = 0 #0이면 선택안됨

    def update(self):
        pass

    def draw(self):
        self.tower1_icon.draw(1280 - 64, 720 - 64)
        if self.left_click == 1:
            if self.cho_tower == 1:
                self.tower1_click.draw(mouse_x, mouse_y)



def enter():
    global ui, boy, monster1

    ui = Ui()
    boy = Boy()
    tile = Tile()
    monster1 = Monster1()

    game_world.add_object(tile, 0)
    game_world.add_object(boy, 1)
    game_world.add_object(monster1, 1)


def exit():
    game_world.clear()


def pause():
    pass
def resume():
    pass


def handle_events():
    global mouse_x
    global mouse_y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

        elif event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, 720 - event.y
        elif event.type == SDL_MOUSEBUTTONDOWN:
            ui.left_click = 1
            if mouse_x >= 1280 - 128 and mouse_x <= 1280:
                if mouse_y >= 720 - 128 and mouse_y <= 720:
                    ui.cho_tower = 1
            else:
                ui.cho_tower = 0
        elif event.type == SDL_MOUSEBUTTONUP:
            ui.left_click = 0

        else:
            boy.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    ui.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    ui.draw()
    update_canvas()






