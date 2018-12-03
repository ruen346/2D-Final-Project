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
                    teemo.hp -= main_state.tower1_d + game_object.damage
                    break
            elif str(game_object).find("elf_arrow") != -1: # elf_arrow와 충돌시
                if game_object.x > teemo.x - 64 and game_object.x < teemo.x + 64 and game_object.y < teemo.y + 64 and  game_object.y > teemo.y - 64:
                    game_world.remove_object(game_object)
                    teemo.hp -= main_state.elf_d
                    break
            elif str(game_object).find("magic") != -1 and str(game_object).find("tower") == -1:  # magic와 충돌시
                if math.sqrt((game_object.x - teemo.x)**2 + (game_object.y - teemo.y)**2) < 250 and get_time() >= teemo.time + 0.1:
                    teemo.hp -= main_state.tower2_d + game_object.damage
                    break
            elif str(game_object).find("boom") != -1: # boom와 충돌시
                if game_object.x > teemo.x - 64 and game_object.x < teemo.x + 64 and game_object.y < teemo.y + 64 and  game_object.y > teemo.y - 64:
                    game_world.remove_object(game_object)
                    from fire import Fire
                    fire = Fire(teemo.x, teemo.y)
                    game_world.add_object(fire, 2)
                    break
            elif str(game_object).find("fire") != -1: # fire와 충돌시
                if math.sqrt((game_object.x - teemo.x)**2 + (game_object.y - teemo.y)**2) < 100 and get_time() >= teemo.time + 0.1:
                    game_world.remove_object(game_object)
                    teemo.hp -= main_state.tower3_d
                    break

        if get_time() >= teemo.time + 0.1: #다단히트 스킬땜시
            teemo.time = get_time()

        if teemo.hp <= 0: #피가 0되서 죽음
            game_world.remove_object(teemo)
            main_state.ui.money += 500

        if teemo.y > 720 + 64: #경로에 나가서 사라짐
            game_world.remove_object(teemo)
            main_state.ui.life -= 1

    @staticmethod
    def draw(teemo):
        teemo.image.draw(teemo.x + main_state.elf_move_window_x, teemo.y + main_state.elf_move_window_y)
        teemo.hp_bar.draw(teemo.x + main_state.elf_move_window_x, teemo.y + main_state.elf_move_window_y + 90)
        teemo.hp_red.clip_draw(2, 2, int(60 * teemo.hp / 10000), 12, teemo.x + main_state.elf_move_window_x, teemo.y + main_state.elf_move_window_y + 90)


class Teemo:

    def __init__(self):
        self.x, self.y = 0, 720-320
        self.image = load_image('image\\teemo_sp_0.png')
        self.hp_bar = load_image('image\\hp_bar.png')
        self.hp_red = load_image('image\\hp_red.png')
        self.move = 1
        self.hp = 10000
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.time = get_time()

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)