from pico2d import *
import game_framework
import main_state

class Tile:
    global ui

    def __init__(self):
        self.tile1_up = load_image('image\\tile1_up.png')


        self.select_sp = load_image('image\\select.png')
        self.in_tower = [0 for i in range(240)] #타워가 타일에 설치되있는지, 없으면 0
        self.time = [0 for i in range(240)]


    def update(self):
        pass


    def draw(self):
        for i in range(240):
            if game_framework.text3[i] == '1':
                self.tile1_up.draw((i % 20) * 128 + 128 + main_state.elf_move_window_x, 720 - (i // 20) * 128 + main_state.elf_move_window_y)
            if game_framework.text3[i] == '5':
                self.tile1_up.draw((i % 20) * 128 + 128 + main_state.elf_move_window_x, 720 - (i // 20) * 128 + main_state.elf_move_window_y)



        if main_state.ui.cho_tower != 0:
            for i in range(240):
                if game_framework.text3[i] == '1' and self.in_tower[i] == 0:
                    self.select_sp.draw((i % 20) * 128 + 128 + main_state.elf_move_window_x, 720 - (i // 20) * 128 + main_state.elf_move_window_y)