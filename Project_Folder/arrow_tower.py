from pico2d import *
import game_world
import main_state
import re
from shot_arrow import Shot_arrow


class Arrow_tower:

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = load_image('tower1.png')
        self.time = get_time()

    def update(self):
        front_monster_x = 0  # 맨앞 몬스터 좌표
        front_monster_y = 720  # 맨앞 몬스터 좌표
        for game_object in game_world.all_objects(): #맨앞 몬스터 위치
            if str(game_object).find("monster1") != -1:
                if front_monster_x < game_object.x:
                    front_monster_x = game_object.x
                if front_monster_y > game_object.y:
                    front_monster_y = game_object.y

        if get_time() - (self.time + 0.5) >= 0.5:
            vector = (abs(front_monster_x - self.x) + abs(self.y - front_monster_y)) / 10
            shot_arrow = Shot_arrow(self.x, self.y, (front_monster_x - self.x) / vector, -(self.y - front_monster_y) / vector)
            game_world.add_object(shot_arrow, 1)
            self.time += 0.5

    def draw(self):
        self.image.draw(self.x,self.y)
