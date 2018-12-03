from pico2d import *
import game_world
import main_state

class Boom:
    image = None

    def __init__(self, x, y, x_vector, y_vector, damage):
        self.image = load_image('image\\ball21x21.png')
        self.x, self.y, self.x_vector, self.y_vector, self.damage = x, y, x_vector, y_vector, damage

    def draw(self):
        self.image.draw(self.x + main_state.elf_move_window_x, self.y + main_state.elf_move_window_y)

    def update(self):
        self.x += self.x_vector
        self.y += self.y_vector

        if self.x < 25 or self.x > 4000 or self.y > 720 or self.y < -2000:
            game_world.remove_object(self)