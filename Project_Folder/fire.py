from pico2d import *
import game_world
import main_state

class Fire:
    image = None

    def __init__(self, x, y):
        self.image = load_image('image\\tower2_skill.png')
        self.x, self.y = x, y
        self.time = get_time()

    def draw(self):
        self.image.draw(self.x + main_state.elf_move_window_x, self.y + main_state.elf_move_window_y)

    def update(self):
        if self.time < get_time() - 0.5:
            game_world.remove_object(self)