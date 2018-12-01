import random
import json
import os

from pico2d import *
import game_framework
import game_world

from elf import Elf
from tile import Tile
from tile_under import Tile_under
from monster1 import Monster1
from monster2 import Monster2
from monster3 import Monster3
from monster4 import Monster4
from boss import Boss
from teemo import Teemo
from arrow_tower import Arrow_tower
from magic_tower import Magic_tower
from buff_tower import Buff_tower


f = open("map\\monster.txt", 'r')
monster_txt = f.read()
monster_spawn = monster_txt.split() #종류,초



mouse_x = 0
mouse_y = 0

elf_move_window_x = 0
elf_move_window_y = 0

stage = 0 #현재 라운드

time = get_time()
stage_time = -5
stage1_time = 0
monster_num = 0

name = "MainState"



class Ui:
    global mouse_x
    global mouse_y
    global stage
    global stage_time

    def __init__(self):
        self.arrow_tower_icon = load_image('image\\tower1_icon.png')
        self.arrow_tower_click = load_image('image\\tower1_click.png')
        self.arrow_tower_range = load_image('image\\arrow_tower_range.png')
        self.magic_tower_icon = load_image('image\\tower2_icon.png')
        self.magic_tower_click = load_image('image\\tower2_click.png')
        self.magic_tower_range = load_image('image\\arrow_tower_range.png')
        self.buff_tower_icon = load_image('image\\tower3_icon.png')
        self.buff_tower_click = load_image('image\\tower3_click.png')
        self.buff_tower_range = load_image('image\\arrow_tower_range.png')

        self.gold_sp = load_image('image\\gold.png')
        self.life_sp = load_image('image\\life.png')
        self.num_sp = [None, None, None, None, None, None, None, None, None, None,]
        self.num_sp[0] = load_image('image\\0.png')
        self.num_sp[1] = load_image('image\\1.png')
        self.num_sp[2] = load_image('image\\2.png')
        self.num_sp[3] = load_image('image\\3.png')
        self.num_sp[4] = load_image('image\\4.png')
        self.num_sp[5] = load_image('image\\5.png')
        self.num_sp[6] = load_image('image\\6.png')
        self.num_sp[7] = load_image('image\\7.png')
        self.num_sp[8] = load_image('image\\8.png')
        self.num_sp[9] = load_image('image\\9.png')
        self.stage_sp = [None, None, None, None, None, None, None]
        self.stage_sp[0] = load_image('image\\stage1.png')
        self.stage_sp[1] = load_image('image\\stage2.png')
        self.stage_sp[2] = load_image('image\\stage3.png')
        self.stage_sp[3] = load_image('image\\stage4.png')
        self.stage_sp[4] = load_image('image\\stage5.png')
        self.stage_sp[5] = load_image('image\\stage6.png')
        self.stage_sp[6] = load_image('image\\stage7.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.money = 100
        self.life = 20

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
            self.arrow_tower_range.draw(self.cho_build_x + elf_move_window_x,self.cho_build_y + elf_move_window_y)

        self.life_sp.draw(52, 668)
        self.gold_sp.draw(52, 584)
        self.num_sp[self.life // 10].draw(108, 664)
        self.num_sp[self.life % 10].draw(140, 664)
        self.num_sp[self.money // 100].draw(108, 580)
        self.num_sp[(self.money - self.money // 100 * 100) // 10].draw(140, 580)
        self.num_sp[self.money % 10].draw(172, 580)

        if get_time() - stage_time < 5:
            self.stage_sp[stage - 1].draw(640,360)


def enter():
    global ui, elf, tile, tile_under, time

    ui = Ui()
    elf = Elf()
    tile = Tile()
    tile_under = Tile_under()
    time = get_time()

    game_world.add_object(tile_under, 0)
    game_world.add_object(tile, 1)
    game_world.add_object(elf, 2)


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
            if mouse_x >= 1280 - 128 and mouse_x <= 1280 and mouse_y >= 720 - 128 and mouse_y <= 720 and ui.money >= 20:
                ui.cho_tower = 1
            else:
                ui.cho_tower = 0

            if tile.in_tower[int((mouse_x - elf_move_window_x - 64) / 128) + (int((720-(mouse_y - elf_move_window_y) + 64) / 128) * 20)] == 1:
                ui.cho_build_tower = 1
                ui.cho_build_x = int((mouse_x - elf_move_window_x - 64) / 128) * 128 + 128
                ui.cho_build_y = int((mouse_y - elf_move_window_y + 128) / 128) * 128 - 64
            else:
                ui.cho_build_tower = 0

        ############################################################################# 마우스 좌클릭 땜
        elif event.type == SDL_MOUSEBUTTONUP:
            if tile.in_tower[int((mouse_x - elf_move_window_x - 64) / 128) + (int((720-(mouse_y - elf_move_window_y) + 64) / 128) * 20)] == 0 and game_framework.text3[int((mouse_x - elf_move_window_x - 64) / 128) + (int((720-(mouse_y - elf_move_window_y) + 64) / 128) * 20)] == '1':
                tile.in_tower[int((mouse_x - elf_move_window_x - 64) / 128) + (int((720-(mouse_y - elf_move_window_y) + 64) / 128) * 20)] = ui.cho_tower
                if(ui.cho_tower == 1): #타워1설치
                    i = int((mouse_x - elf_move_window_x - 64) / 128) + (int((720-(mouse_y - elf_move_window_y) + 64) / 128) * 20)
                    arrow_tower = Arrow_tower(i)
                    game_world.add_object(arrow_tower, 2)
                    tile.time[i] = int(get_time())
                    ui.money -= 20 # 돈차감
            ui.left_click = 0
            ui.cho_tower = 0

        else:
            elf.handle_event(event)


def update():
    global time, monster1, monster2, monster3, monster4, boss, teemo, stage_time, stage1_time, stage, monster_num, monster_spawn

    for game_object in game_world.all_objects():
        game_object.update()
    ui.update()


    if get_time() - time >= 10 and stage == 0: #10초후 게임 시작
        stage = 1
        monster_num = 0
        stage_time = get_time()
        stage1_time = get_time()

    if stage >= 1:
        if get_time() - stage1_time >= int(monster_spawn[monster_num + 1]):
            if int(monster_spawn[monster_num]) == 1:
                monster1 = Monster1()
                game_world.add_object(monster1, 0)
            elif int(monster_spawn[monster_num]) == 2:
                monster2 = Monster2()
                game_world.add_object(monster2, 0)
            elif int(monster_spawn[monster_num]) == 3:
                monster3 = Monster3()
                game_world.add_object(monster3, 0)
            elif int(monster_spawn[monster_num]) == 4:
                monster4 = Monster4()
                game_world.add_object(monster4, 0)
            elif int(monster_spawn[monster_num]) == 5:
                boss = Boss()
                game_world.add_object(boss, 0)
            elif int(monster_spawn[monster_num]) == 6:
                teemo = Teemo()
                game_world.add_object(teemo, 0)

            elif int(monster_spawn[monster_num]) == 9:
                stage += 1
                stage_time = get_time()

            monster_num += 2


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    ui.draw()
    update_canvas()






