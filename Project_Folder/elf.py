import game_framework
from pico2d import *
from shot_arrow import Ball

import random
import math

import game_world

# Elf Run Speed
PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Elf Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


# Elf Event
RIGHT_DOWN, LEFT_DOWN, UP_DOWN, DOWN_DOWN, RIGHT_UP, LEFT_UP, UP_UP, DOWN_UP, SPACE = range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}


class IdleState:

    @staticmethod
    def enter(elf, event):
        if event == RIGHT_DOWN:
            elf.width += RUN_SPEED_PPS
        if event == LEFT_DOWN:
            elf.width -= RUN_SPEED_PPS
        if event == UP_DOWN:
            elf.high += RUN_SPEED_PPS
        if event == DOWN_DOWN:
            elf.high -= RUN_SPEED_PPS
        if event == RIGHT_UP:
            elf.width -= RUN_SPEED_PPS
        if event == LEFT_UP:
            elf.width += RUN_SPEED_PPS
        if event == UP_UP:
            elf.high -= RUN_SPEED_PPS
        if event == DOWN_UP:
            elf.high += RUN_SPEED_PPS
        elf.timer = get_time()

    @staticmethod
    def exit(elf, event):
        if event == SPACE:
            elf.fire_ball()
        pass

    @staticmethod
    def do(elf):
        pass

    @staticmethod
    def draw(elf):
        elf.image.draw(elf.x, elf.y)


class RunState:

    @staticmethod
    def enter(elf, event):
        if event == RIGHT_DOWN:
            elf.width += RUN_SPEED_PPS
        if event == LEFT_DOWN:
            elf.width -= RUN_SPEED_PPS
        if event == UP_DOWN:
            elf.high += RUN_SPEED_PPS
        if event == DOWN_DOWN:
            elf.high -= RUN_SPEED_PPS
        if event == RIGHT_UP:
            elf.width -= RUN_SPEED_PPS
        if event == LEFT_UP:
            elf.width += RUN_SPEED_PPS
        if event == UP_UP:
            elf.high -= RUN_SPEED_PPS
        if event == DOWN_UP:
            elf.high += RUN_SPEED_PPS

    @staticmethod
    def exit(elf, event):
        if event == SPACE:
            elf.fire_ball()

    @staticmethod
    def do(elf):
        if game_framework.text3[int((elf.x + (elf.width * game_framework.frame_time) - 64) / 128) + (int((720 - elf.y + 128) / 128) * 10)] == '1':
            elf.x += elf.width * game_framework.frame_time
        if game_framework.text3[int((elf.x - 64) / 128) + (int((720 - (elf.y + (elf.high * game_framework.frame_time)) + 128) / 128) * 10)] == '1':
            elf.y += elf.high * game_framework.frame_time

    @staticmethod
    def draw(elf):
        elf.image.draw(elf.x, elf.y)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, UP_UP: RunState, DOWN_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, UP_DOWN: RunState, DOWN_DOWN: RunState, SPACE: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, UP_UP: IdleState, DOWN_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, UP_DOWN: IdleState, DOWN_DOWN: IdleState, SPACE: RunState},
}

class Elf:

    def __init__(self):
        self.x, self.y = 128 * 4, 720 - 64
        self.image = load_image('character_right_stand0.png')
        self.width = 0
        self.high = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def fire_ball(self):
        ball = Ball(self.x, self.y, 0)
        game_world.add_object(ball, 1)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)