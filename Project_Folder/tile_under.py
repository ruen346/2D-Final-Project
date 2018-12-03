from pico2d import *
import game_framework
import main_state

class Tile_under:
    global ui

    def __init__(self):
        self.tile1 = load_image("image\\tile5.png")
        self.tile2 = load_image('image\\tile2.png')
        self.tile3 = load_image('image\\tile3.png')
        self.tile4 = [None, None, None, None, None, None]
        self.tile4[0] = load_image('image\\tile4_high.png')
        self.tile4[1] = load_image('image\\tile4_LD.png')
        self.tile4[2] = load_image('image\\tile4_LU.png')
        self.tile4[3] = load_image('image\\tile4_RD.png')
        self.tile4[4] = load_image('image\\tile4_RU.png')
        self.tile4[5] = load_image('image\\tile4_width.png')

        self.tile1_left = load_image('image\\tile1_left.png')
        self.tile1_down = load_image('image\\tile1_down.png')

    def update(self):
        pass


    def draw(self):
        for i in range(240):
            if game_framework.text2[i] == '1':
                self.tile1.draw((i % 20) * 128 + 64 + main_state.elf_move_window_x, 720 - (i // 20) * 128 - 64 + main_state.elf_move_window_y)
            elif game_framework.text2[i] == '2':
                self.tile2.draw((i % 20) * 128 + 64 + main_state.elf_move_window_x, 720 - (i // 20) * 128 - 64 + main_state.elf_move_window_y)
            elif game_framework.text2[i] == '3':
                self.tile3.draw((i % 20) * 128 + 64 + main_state.elf_move_window_x, 720 - (i // 20) * 128 - 64 + main_state.elf_move_window_y)
            elif game_framework.text2[i] == '4':
                self.tile4[0].draw((i % 20) * 128 + 64 + main_state.elf_move_window_x, 720 - (i // 20) * 128 - 64 + main_state.elf_move_window_y)
            elif game_framework.text2[i] == '5':
                self.tile4[1].draw((i % 20) * 128 + 64 + main_state.elf_move_window_x, 720 - (i // 20) * 128 - 64 + main_state.elf_move_window_y)
            elif game_framework.text2[i] == '6':
                self.tile4[2].draw((i % 20) * 128 + 64 + main_state.elf_move_window_x, 720 - (i // 20) * 128 - 64 + main_state.elf_move_window_y)
            elif game_framework.text2[i] == '7':
                self.tile4[3].draw((i % 20) * 128 + 64 + main_state.elf_move_window_x, 720 - (i // 20) * 128 - 64 + main_state.elf_move_window_y)
            elif game_framework.text2[i] == '8':
                self.tile4[4].draw((i % 20) * 128 + 64 + main_state.elf_move_window_x, 720 - (i // 20) * 128 - 64 + main_state.elf_move_window_y)
            elif game_framework.text2[i] == '9':
                self.tile4[5].draw((i % 20) * 128 + 64 + main_state.elf_move_window_x, 720 - (i // 20) * 128 - 64 + main_state.elf_move_window_y)
                
        for i in range(240):
            if game_framework.text3[i] == '2':
                self.tile1_left.draw((i % 20) * 128 + 160 + main_state.elf_move_window_x, 720 - (i // 20) * 128 - 32 + main_state.elf_move_window_y)
            elif game_framework.text3[i] == '3':
                self.tile1_down.draw((i % 20) * 128 + 96 + main_state.elf_move_window_x, 720 - (i // 20) * 128 + 32 + main_state.elf_move_window_y)
            elif game_framework.text3[i] == '4':
                self.tile1_left.draw((i % 20) * 128 + 160 + main_state.elf_move_window_x, 720 - (i // 20) * 128 - 32 + main_state.elf_move_window_y)
                self.tile1_down.draw((i % 20) * 128 + 96 + main_state.elf_move_window_x, 720 - (i // 20) * 128 + 32 + main_state.elf_move_window_y)