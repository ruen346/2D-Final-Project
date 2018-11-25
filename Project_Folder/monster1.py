import game_framework
from pico2d import *
import game_world
import main_state

PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class IdleState:

    @staticmethod
    def enter(monster1, event):
        monster1.timer = get_time()

    @staticmethod
    def exit(monster1, event):
        pass

    @staticmethod
    def do(monster1):
        if monster1.move == 1 and monster1.x >= 128 * 6 - 64:
            monster1.move = 2
        elif monster1.move == 2 and monster1.y <= 720 - (128 * 10 - 64):
            monster1.move = 3
        elif monster1.move == 3 and monster1.x >= 128 * 18 - 64:
            monster1.move = 4
        elif monster1.move == 4 and monster1.y >= 720 - (128 * 7 - 64):
            monster1.move = 5
        elif monster1.move == 5 and monster1.x <= 128 * 12 - 64:
            monster1.move = 6

        if monster1.move == 1:
            monster1.x += 1.5
        elif monster1.move == 2:
            monster1.y -= 1.5
        elif monster1.move == 3:
            monster1.x += 1.5
        elif monster1.move == 4:
            monster1.y += 1.5
        elif monster1.move == 5:
            monster1.x -= 1.5
        elif monster1.move == 6:
            monster1.y += 1.5

        for game_object in game_world.all_objects():
            if str(game_object).find("shot_arrow") != -1: # shot_arrow와 충돌시
                if game_object.x > monster1.x - 64 and game_object.x < monster1.x + 64 and game_object.y < monster1.y + 64 and  game_object.y > monster1.y - 46:
                    game_world.remove_object(game_object)
                    monster1.hp -= 40
                    break
            elif str(game_object).find("elf_arrow") != -1: # elf_arrow와 충돌시
                if game_object.x > monster1.x - 64 and game_object.x < monster1.x + 64 and game_object.y < monster1.y + 32 and  game_object.y > monster1.y - 46:
                    game_world.remove_object(game_object)
                    monster1.hp -= 40
                    break

        if monster1.hp <= 0:
            game_world.remove_object(monster1)
            main_state.ui.money += 10

        if monster1.y > 720 + 64: #나가면 사라짐
            game_world.remove_object(monster1)
            main_state.ui.life -= 1

    @staticmethod
    def draw(monster1):
        monster1.image.draw(monster1.x + main_state.elf_move_window_x, monster1.y + main_state.elf_move_window_y)


class Monster1:

    def __init__(self):
        self.x, self.y = 0, 720-320
        self.image = load_image('image\\monster1.png')
        self.move = 1
        self.hp = 100
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)


