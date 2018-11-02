import random
import json
import os

from pico2d import *

import game_framework
import title_state
import main_state



name = "PauseState"

pauses = None
font = None


class Pause:
    def __init__(self):
        self.frame = 0

    def update(self):
        if self.frame == 50:
            self.frame = 0
        else:
            self.frame += 1

    def draw(self):
        if self.frame > 25:
            load_image('pause.png').draw(400, 400)


def enter():
    global pauses
    pauses = Pause()


def exit():
    global pauses
    del (pauses)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT: game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.pop_state()


def update():
    pauses.update()


def draw():
    clear_canvas()
    main_state.grass.draw()
    main_state.boy.draw()
    pauses.draw()


    update_canvas()