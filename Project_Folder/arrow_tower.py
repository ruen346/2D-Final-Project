from pico2d import *
import game_world
import main_state
from shot_arrow import Shot_arrow


class Arrow_tower:

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = load_image('tower1.png')
        self.time = get_time()

    def update(self):
        if get_time() - (self.time + 0.5) >= 0.5:
            vector = (abs(main_state.front_monster_x - self.x) + abs(self.y - main_state.front_monster_y)) / 10
            shot_arrow = Shot_arrow(self.x, self.y, (main_state.front_monster_x - self.x) / vector, -(self.y - main_state.front_monster_y) / vector)
            game_world.add_object(shot_arrow, 1)
            self.time += 0.5

    def draw(self):
        self.image.draw(self.x,self.y)
