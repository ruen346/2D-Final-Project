import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from tile import Tile
from monster1 import Monster1


name = "MainState"

boy = None
monster1 = None

def enter():
    global boy, monster1

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
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            boy.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()



def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






