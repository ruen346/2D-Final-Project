from pico2d import *
import game_world
import main_state

class Fire:
    image = None

    def __init__(self, x, y, damage):
        self.image = load_image('image\\fire.png')
        self.x, self.y, self.damage = x, y, damage
        self.time = get_time()
        self.sound = load_wav('sound\\boom.wav')
        self.sound.set_volume(46)
        self.sound.play()

    def draw(self):
        self.image.draw(self.x + main_state.elf_move_window_x, self.y + main_state.elf_move_window_y)

    def update(self):
        if self.time < get_time() - 0.5:
            game_world.remove_object(self)