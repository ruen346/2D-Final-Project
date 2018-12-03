from pico2d import *
import game_world
import main_state
import math
from magic import Magic


class Magic_tower:

    def __init__(self, i):
        self.x, self.y = (i % 20) * 128 + 128, 720 - (i // 20) * 128
        self.image = load_image('image\\tower2.png')
        self.time = get_time()
        self.upgrade = 0
        self.damage = 0

    def update(self):
        if self.upgrade >= 1:
            self.damage = 10

        for game_object in game_world.all_objects(): #맨앞 몬스터 위치
            if str(game_object).find("monster1") != -1 or str(game_object).find("monster2") != -1 or str(game_object).find("monster3") != -1 or str(game_object).find("monster4") != -1 or str(game_object).find("boss") != -1 or str(game_object).find("teemo") != -1:
                if math.sqrt((game_object.x - self.x)**2 + (game_object.y - self.y)**2) < 250:
                    if get_time() >= self.time + 1.5:  # 마법 사용
                        magic = Magic(self.x, self.y, self.damage)
                        game_world.add_object(magic, 2)
                        self.time = get_time()


    def draw(self):
        self.image.draw(self.x + main_state.elf_move_window_x, self.y + main_state.elf_move_window_y)
