import game_framework
from pico2d import *
import game_world
import main_state

PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 15.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class IdleState:

    @staticmethod
    def enter(teemo, event):
        teemo.timer = get_time()

    @staticmethod
    def exit(teemo, event):
        pass

    @staticmethod
    def do(teemo):
        if teemo.move == 1 and teemo.x >= 128 * 6 - 64:
            teemo.move = 2
        elif teemo.move == 2 and teemo.y <= 720 - (128 * 10 - 64):
            teemo.move = 3
        elif teemo.move == 3 and teemo.x >= 128 * 18 - 64:
            teemo.move = 4
        elif teemo.move == 4 and teemo.y >= 720 - (128 * 7 - 64):
            teemo.move = 5
        elif teemo.move == 5 and teemo.x <= 128 * 12 - 64:
            teemo.move = 6

        if teemo.move == 1:
            teemo.x += 1.5
        elif teemo.move == 2:
            teemo.y -= 1.5
        elif teemo.move == 3:
            teemo.x += 1.5
        elif teemo.move == 4:
            teemo.y += 1.5
        elif teemo.move == 5:
            teemo.x -= 1.5
        elif teemo.move == 6:
            teemo.y += 1.5

        for game_object in game_world.all_objects():
            if str(game_object).find("shot_arrow") != -1: # shot_arrow와 충돌시
                if game_object.x > teemo.x - 64 and game_object.x < teemo.x + 64 and game_object.y < teemo.y + 64 and  game_object.y > teemo.y - 64:
                    game_world.remove_object(game_object)
                    teemo.hp -= 40
                    break
            elif str(game_object).find("elf_arrow") != -1: # elf_arrow와 충돌시
                if game_object.x > teemo.x - 64 and game_object.x < teemo.x + 64 and game_object.y < teemo.y + 64 and  game_object.y > teemo.y - 64:
                    game_world.remove_object(game_object)
                    teemo.hp -= 40
                    break

        if teemo.hp <= 0: #피가 0되서 죽음
            game_world.remove_object(teemo)
            main_state.ui.money += 15

        if teemo.y > 720 + 64: #경로에 나가서 사라짐
            game_world.remove_object(teemo)
            main_state.ui.life -= 1

    @staticmethod
    def draw(teemo):
        teemo.image.draw(teemo.x + main_state.elf_move_window_x, teemo.y + main_state.elf_move_window_y)


class Teemo:

    def __init__(self):
        self.x, self.y = 0, 720-320
        self.image = load_image('image\\teemo_sp_0.png')
        self.move = 1
        self.hp = 800
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)