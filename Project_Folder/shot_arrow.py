from pico2d import *
import game_world
import main_state

class Shot_arrow:
    image = None

    def __init__(self, x, y, x_vector, y_vector):
        self.image = load_image('image\\ball21x21.png')
        self.x, self.y, self.x_vector, self.y_vector = x, y, x_vector, y_vector

    def draw(self):
        self.image.draw(self.x + main_state.elf_move_window_x, self.y + main_state.elf_move_window_y)

    def update(self):
        self.x += self.x_vector
        self.y += self.y_vector

        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)
