from pico2d import *
import game_world
from shot_arrow import Shot_arrow


class Arrow_tower:

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = load_image('tower1.png')
        self.time = get_time()

    def update(self):
        if get_time() - (self.time + 1) >= 1:
            shot_arrow = Shot_arrow(self.x, self.y, 10, 10)
            game_world.add_object(shot_arrow, 1)
            self.time += 1

    def draw(self):
        self.image.draw(self.x,self.y)


