from pico2d import *
import game_framework
import main_state

class Tile:
    global ui

    def __init__(self):
        self.tile1 = load_image("tile5.png")
        self.tile2 = load_image('tile2.png')
        self.tile3 = load_image('tile3.png')
        self.tile1_up = load_image('tile1_up.png')
        self.tile1_left = load_image('tile1_left.png')
        self.tile1_down = load_image('tile1_down.png')
        self.tile4 = [None, None, None, None, None, None]
        self.tile4[0] = load_image('tile4_high.png')
        self.tile4[1] = load_image('tile4_LD.png')
        self.tile4[2] = load_image('tile4_LU.png')
        self.tile4[3] = load_image('tile4_RD.png')
        self.tile4[4] = load_image('tile4_RU.png')
        self.tile4[5] = load_image('tile4_width.png')

        self.select_sp = load_image('select.png')
        self.in_tower = [i for i in range(60)]



    def update(self):
        pass


    def draw(self):
        for i in range(60):
            if game_framework.text2[i] == '1':
                self.tile1.draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)
            elif game_framework.text2[i] == '2':
                self.tile2.draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)
            elif game_framework.text2[i] == '3':
                self.tile3.draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)
            elif game_framework.text2[i] == '4':
                self.tile4[0].draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)
            elif game_framework.text2[i] == '5':
                self.tile4[1].draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)
            elif game_framework.text2[i] == '6':
                self.tile4[2].draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)
            elif game_framework.text2[i] == '7':
                self.tile4[3].draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)
            elif game_framework.text2[i] == '8':
                self.tile4[4].draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)
            elif game_framework.text2[i] == '9':
                self.tile4[5].draw((i % 10) * 128 + 64, 720 - (i // 10) * 128 - 64)

        for i in range(60):
            if game_framework.text3[i] == '1':
                self.tile1_up.draw((i % 10) * 128 + 128, 720 - (i // 10) * 128)
            elif game_framework.text3[i] == '2':
                self.tile1_left.draw((i % 10) * 128 + 160, 720 - (i // 10) * 128 - 32)
            elif game_framework.text3[i] == '3':
                self.tile1_down.draw((i % 10) * 128 + 96, 720 - (i // 10) * 128 + 32)
            elif game_framework.text3[i] == '4':
                self.tile1_left.draw((i % 10) * 128 + 160, 720 - (i // 10) * 128 - 32)
                self.tile1_down.draw((i % 10) * 128 + 96, 720 - (i // 10) * 128 + 32)

        if main_state.ui.cho_tower != 0:
            for i in range(60):
                if game_framework.text3[i] == '1':
                    self.select_sp.draw((i % 10) * 128 + 128, 720 - (i // 10) * 128)
