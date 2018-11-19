import game_framework
import title_state
from pico2d import *


name = "StartState"
image = None
logo_time = get_time()


def enter():
    global image
    image = load_image('image\\kpu_credit.png')


def exit():
    global image
    del (image)


def handle_events():
    pass


def update():
    global logo_time
    if (get_time() - logo_time > 1.0):
        game_framework.change_state(title_state)


def draw():
    global image
    clear_canvas()
    image.draw(640, 360)
    update_canvas()