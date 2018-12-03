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
    def enter(monster4, event):
        monster4.timer = get_time()

    @staticmethod
    def exit(monster4, event):
        pass

    @staticmethod
    def do(monster4):
        if monster4.move == 1 and monster4.x >= 128 * 6 - 64:
            monster4.move = 2
        elif monster4.move == 2 and monster4.y <= 720 - (128 * 10 - 64):
            monster4.move = 3
        elif monster4.move == 3 and monster4.x >= 128 * 18 - 64:
            monster4.move = 4
        elif monster4.move == 4 and monster4.y >= 720 - (128 * 7 - 64):
            monster4.move = 5
        elif monster4.move == 5 and monster4.x <= 128 * 12 - 64:
            monster4.move = 6

        if monster4.move == 1:
            monster4.x += 1.5
        elif monster4.move == 2:
            monster4.y -= 1.5
        elif monster4.move == 3:
            monster4.x += 1.5
        elif monster4.move == 4:
            monster4.y += 1.5
        elif monster4.move == 5:
            monster4.x -= 1.5
        elif monster4.move == 6:
            monster4.y += 1.5

        for game_object in game_world.all_objects():
            if str(game_object).find("shot_arrow") != -1: # shot_arrow와 충돌시
                if game_object.x > monster4.x - 64 and game_object.x < monster4.x + 64 and game_object.y < monster4.y + 64 and  game_object.y > monster4.y - 64:
                    game_world.remove_object(game_object)
                    monster4.hp -= main_state.tower1_d
                    break
            elif str(game_object).find("elf_arrow") != -1: # elf_arrow와 충돌시
                if game_object.x > monster4.x - 64 and game_object.x < monster4.x + 64 and game_object.y < monster4.y + 64 and  game_object.y > monster4.y - 64:
                    game_world.remove_object(game_object)
                    monster4.hp -= main_state.elf_d
                    break
            elif str(game_object).find("magic") != -1: # magic와 충돌시
                if math.sqrt((game_object.x - monster4.x)**2 + (game_object.y - monster4.y)**2) < 250 and get_time() >= monster4.time + 0.1:
                    monster4.hp -= 20
                    break
            elif str(game_object).find("boom") != -1: # boom와 충돌시
                if game_object.x > monster4.x - 64 and game_object.x < monster4.x + 64 and game_object.y < monster4.y + 64 and  game_object.y > monster4.y - 64:
                    game_world.remove_object(game_object)
                    from fire import Fire
                    fire = Fire(monster4.x, monster4.y)
                    game_world.add_object(fire, 2)
                    break
            elif str(game_object).find("fire") != -1: # fire와 충돌시
                if math.sqrt((game_object.x - monster4.x)**2 + (game_object.y - monster4.y)**2) < 100 and get_time() >= monster4.time + 0.1:
                    game_world.remove_object(game_object)
                    monster4.hp -= main_state.tower3_d
                    break

        if get_time() >= monster4.time + 0.1: #다단히트 스킬땜시
            monster4.time = get_time()

        if monster4.hp <= 0: #피가 0되서 죽음
            game_world.remove_object(monster4)
            main_state.ui.money += 25

        if monster4.y > 720 + 64: #경로에 나가서 사라짐
            game_world.remove_object(monster4)
            main_state.ui.life -= 1

    @staticmethod
    def draw(monster4):
        monster4.image.draw(monster4.x + main_state.elf_move_window_x, monster4.y + main_state.elf_move_window_y)


class Monster4:

    def __init__(self):
        self.x, self.y = 0, 720-320
        self.image = load_image('image\\monster4.png')
        self.hp_bar = load_image('image\\hp_bar.png')
        self.hp_red = load_image('image\\hp_red.png')
        self.move = 1
        self.hp = 800
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.time = get_time()

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)