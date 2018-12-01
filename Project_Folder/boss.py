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
    def enter(boss, event):
        boss.timer = get_time()

    @staticmethod
    def exit(boss, event):
        pass

    @staticmethod
    def do(boss):
        if boss.move == 1 and boss.x >= 128 * 6 - 64:
            boss.move = 2
        elif boss.move == 2 and boss.y <= 720 - (128 * 10 - 64):
            boss.move = 3
        elif boss.move == 3 and boss.x >= 128 * 18 - 64:
            boss.move = 4
        elif boss.move == 4 and boss.y >= 720 - (128 * 7 - 64):
            boss.move = 5
        elif boss.move == 5 and boss.x <= 128 * 12 - 64:
            boss.move = 6

        if boss.move == 1:
            boss.x += 1.5
        elif boss.move == 2:
            boss.y -= 1.5
        elif boss.move == 3:
            boss.x += 1.5
        elif boss.move == 4:
            boss.y += 1.5
        elif boss.move == 5:
            boss.x -= 1.5
        elif boss.move == 6:
            boss.y += 1.5

        for game_object in game_world.all_objects():
            if str(game_object).find("shot_arrow") != -1: # shot_arrow와 충돌시
                if game_object.x > boss.x - 64 and game_object.x < boss.x + 64 and game_object.y < boss.y + 64 and  game_object.y > boss.y - 64:
                    game_world.remove_object(game_object)
                    boss.hp -= 40
                    break
            elif str(game_object).find("elf_arrow") != -1: # elf_arrow와 충돌시
                if game_object.x > boss.x - 64 and game_object.x < boss.x + 64 and game_object.y < boss.y + 64 and  game_object.y > boss.y - 64:
                    game_world.remove_object(game_object)
                    boss.hp -= 40
                    break

        if boss.hp <= 0: #피가 0되서 죽음
            game_world.remove_object(boss)
            main_state.ui.money += 15

        if boss.y > 720 + 64: #경로에 나가서 사라짐
            game_world.remove_object(boss)
            main_state.ui.life -= 1

    @staticmethod
    def draw(boss):
        boss.image.draw(boss.x + main_state.elf_move_window_x, boss.y + main_state.elf_move_window_y)


class Boss:

    def __init__(self):
        self.x, self.y = 0, 720-320
        self.image = load_image('image\\monster1.png')
        self.move = 1
        self.hp = 800
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)