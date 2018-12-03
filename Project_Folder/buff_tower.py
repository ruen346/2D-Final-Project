from pico2d import *
import game_world
import main_state
import math
from boom import Boom


class Buff_tower:

    def __init__(self, i):
        self.x, self.y = (i % 20) * 128 + 128, 720 - (i // 20) * 128
        self.image = load_image('image\\tower3.png')
        self.time = get_time()
        self.upgrade = 0
        self.delay = 1.5
        self.damage = 0
        self.speeds = 5
        self.sound = load_wav('sound\\shot.wav')
        self.sound.set_volume(100)

    def update(self):
        if self.upgrade >= 1:
            self.delay = 1
        if self.upgrade == 2:
            self.damage = 15
        if self.upgrade == 3:
            self.speeds = 25

        front_monster_x = 0  # 맨앞 몬스터 좌표
        front_monster_y = 720  # 맨앞 몬스터 좌표
        front_monster_move = 0 # 맨앞 몬스터 어디경로 이동
        for game_object in game_world.all_objects(): #맨앞 몬스터 위치
            if str(game_object).find("monster1") != -1 or str(game_object).find("monster2") != -1 or str(game_object).find("monster3") != -1 or str(game_object).find("monster4") != -1 or str(game_object).find("boss") != -1 or str(game_object).find("teemo") != -1:
                if math.sqrt((game_object.x - self.x)**2 + (game_object.y - self.y)**2) < 350:
                    if game_object.move > front_monster_move:
                        front_monster_x = game_object.x
                        front_monster_y = game_object.y

        if get_time() >= self.time + self.delay: #대포발사
            if front_monster_y != 720: #없으면 대포 발사 x
                vector = (abs(front_monster_x - self.x) + abs(self.y - front_monster_y)) / self.speeds
                boom = Boom(self.x, self.y, (front_monster_x - self.x) / vector, (front_monster_y - self.y) / vector, self.damage)
                game_world.add_object(boom, 2)
                self.time = get_time()
                self.sound.play()

    def draw(self):
        self.image.draw(self.x + main_state.elf_move_window_x, self.y + main_state.elf_move_window_y)
