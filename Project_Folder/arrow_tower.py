from pico2d import *
import game_world
from ball import Ball


class Arrow_tower:

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = load_image('tower1.png')
        self.time = get_time()

    def update(self):
        if get_time() - (self.time + 1) >= 1:
            ball = Ball(self.x, self.y, 5)
            game_world.add_object(ball, 1)
            self.time += 1

    def draw(self):
        self.image.draw(self.x,self.y)


