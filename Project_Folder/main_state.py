import random
import json
import os

from pico2d import *
import game_framework
import game_world

from elf import Elf
from tile import Tile
from monster1 import Monster1
from arrow_tower import Arrow_tower

mouse_x = 0
mouse_y = 0

time = 0

name = "MainState"

elf = None
monster1 = None
tile = None


class Ui:
    global mouse_x
    global mouse_y

    def __init__(self):
        self.arrow_tower_icon = load_image('tower1_icon.png')
        self.arrow_tower_click = load_image('tower1_click.png')
        self.arrow_tower_range = load_image('arrow_tower_range.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.money = 100
        self.life = 10

        self.left_click = 0 #왼쪽 마우스 누르면 1
        self.cho_tower = 0 #0이면 선택안됨, 어떤 타워 아이콘 눌렀는지
        self.cho_build_tower = 0 #0이면 선택안됨, 어떤 설치된 타워를 눌렀는지
        self.cho_build_x = 0 #설치된 타워 눌렀을때 좌표x
        self.cho_build_y = 0 #설치된 타워 눌렀을때 좌표y

    def update(self):
        pass

    def draw(self):
        self.arrow_tower_icon.draw(1280 - 64, 720 - 64)

        if self.left_click == 1:#좌클릭
            if self.cho_tower == 1:#타워1선택
                self.arrow_tower_range.draw(mouse_x,mouse_y)
                self.arrow_tower_click.draw(mouse_x, mouse_y)

        if self.cho_build_tower == 1:
            self.arrow_tower_range.draw(self.cho_build_x,self.cho_build_y)

        self.font.draw(1200, 50, str(self.money) + 'G', (0, 0, 0))
        self.font.draw(1200, 80, str(self.life) + 'Life', (0, 0, 0))



def enter():
    global ui, elf, monster1, tile, time

    ui = Ui()
    elf = Elf()
    tile = Tile()
    monster1 = Monster1()
    time = get_time()

    game_world.add_object(tile, 0)
    game_world.add_object(elf, 1)
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

        ############################################################################# 마우스 움직임
        elif event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, 720 - event.y

        ############################################################################# 마우스 좌클릭
        elif event.type == SDL_MOUSEBUTTONDOWN:
            ui.left_click = 1
            if mouse_x >= 1280 - 128 and mouse_x <= 1280:
                if mouse_y >= 720 - 128 and mouse_y <= 720:
                    ui.cho_tower = 1
            else:
                ui.cho_tower = 0

            if tile.in_tower[int((mouse_x - 64) / 128) + (int((720-mouse_y + 64) / 128) * 10)] == 1:
                ui.cho_build_tower = 1
                ui.cho_build_x = int((mouse_x - 64) / 128) * 128 + 128
                ui.cho_build_y = int((mouse_y + 128) / 128) * 128 - 64
            else:
                ui.cho_build_tower = 0

        ############################################################################# 마우스 좌클릭 땜
        elif event.type == SDL_MOUSEBUTTONUP:
            if tile.in_tower[int((mouse_x - 64) / 128) + (int((720-mouse_y + 64) / 128) * 10)] == 0 and game_framework.text3[int((mouse_x - 64) / 128) + (int((720-mouse_y + 64) / 128) * 10)] == '1':
                tile.in_tower[int((mouse_x - 64) / 128) + (int((720-mouse_y + 64) / 128) * 10)] = ui.cho_tower
                if(ui.cho_tower == 1): #타워1설치
                    arrow_tower = Arrow_tower(int((mouse_x - 64) / 128) * 128 + 128, int((mouse_y + 64) / 128 + 0.5) * 128)
                    game_world.add_object(arrow_tower, 1)
                    tile.time[int((mouse_x - 64) / 128) + (int((720-mouse_y + 64) / 128) * 10)] = int(get_time())
            print(int(mouse_x / 128) + (int((720-mouse_y + 64) / 128) * 10))
            ui.left_click = 0
            ui.cho_tower = 0

        else:
            elf.handle_event(event)


def update():
    global time, monster1

    for game_object in game_world.all_objects():
        game_object.update()
    ui.update()

    if get_time() - (time + 2) >= 2:
        monster1 = Monster1()
        game_world.add_object(monster1, 1)
        time += 2

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    ui.draw()
    update_canvas()






