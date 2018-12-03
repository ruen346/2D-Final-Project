from pico2d import *
import game_world
import main_state

class Magic:
    image = None

    def __init__(self, x, y, damage, delays):
        self.image = load_image('image\\tower2_skill.png')
        self.x, self.y, self.damage, self.delays = x, y, damage, delays
        self.time = get_time()

    def draw(self):
        self.image.draw(self.x + main_state.elf_move_window_x, self.y + main_state.elf_move_window_y)

    def update(self):
        if self.time < get_time() - self.delays:
            game_world.remove_object(self)