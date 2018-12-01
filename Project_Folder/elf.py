import game_framework
from pico2d import *
import game_world
import main_state
from elf_arrow import Elf_arrow

# Elf Run Speed
PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Elf Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


# Elf Event
RIGHT_DOWN, LEFT_DOWN, UP_DOWN, DOWN_DOWN, RIGHT_UP, LEFT_UP, UP_UP, DOWN_UP = range(8)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP,
}


class IdleState:

    @staticmethod
    def enter(elf, event):
        if event == RIGHT_DOWN:
            elf.width += RUN_SPEED_PPS
        if event == LEFT_DOWN:
            elf.width -= RUN_SPEED_PPS
        if event == UP_DOWN:
            elf.high += RUN_SPEED_PPS
        if event == DOWN_DOWN:
            elf.high -= RUN_SPEED_PPS
        if event == RIGHT_UP:
            elf.width -= RUN_SPEED_PPS
        if event == LEFT_UP:
            elf.width += RUN_SPEED_PPS
        if event == UP_UP:
            elf.high -= RUN_SPEED_PPS
        if event == DOWN_UP:
            elf.high += RUN_SPEED_PPS
        elf.timer = get_time()

    @staticmethod
    def exit(elf, event):
        pass

    @staticmethod
    def do(elf):
        pass

    @staticmethod
    def draw(elf):
        if get_time() % 2 <= 1.85:
            elf.stand0_image.draw(elf.x + main_state.elf_move_window_x, elf.y + main_state.elf_move_window_y)
        else:
            elf.stand1_image.draw(elf.x + main_state.elf_move_window_x, elf.y + main_state.elf_move_window_y)


class RunState:

    @staticmethod
    def enter(elf, event):
        if event == RIGHT_DOWN:
            elf.width += RUN_SPEED_PPS
            elf.look_vector = 3
        if event == LEFT_DOWN:
            elf.width -= RUN_SPEED_PPS
            elf.look_vector = 2
        if event == UP_DOWN:
            elf.high += RUN_SPEED_PPS
            elf.look_vector = 0
        if event == DOWN_DOWN:
            elf.high -= RUN_SPEED_PPS
            elf.look_vector = 1
        if event == RIGHT_UP:
            elf.width -= RUN_SPEED_PPS
        if event == LEFT_UP:
            elf.width += RUN_SPEED_PPS
        if event == UP_UP:
            elf.high -= RUN_SPEED_PPS
        if event == DOWN_UP:
            elf.high += RUN_SPEED_PPS

    @staticmethod
    def exit(elf, event):
        pass

    @staticmethod
    def do(elf):
        if game_framework.text3[int((elf.x + (elf.width * game_framework.frame_time) - 64) / 128) + (int((720 - elf.y + 128) / 128) * 20)] == '1':
            elf.x += elf.width * game_framework.frame_time
        if game_framework.text3[int((elf.x - 64) / 128) + (int((720 - (elf.y + (elf.high * game_framework.frame_time)) + 128) / 128) * 20)] == '1':
            elf.y += elf.high * game_framework.frame_time

    @staticmethod
    def draw(elf):
        elf.stand0_image.draw(elf.x + main_state.elf_move_window_x, elf.y + main_state.elf_move_window_y)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, UP_UP: RunState, DOWN_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, UP_DOWN: RunState, DOWN_DOWN: RunState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, UP_UP: IdleState, DOWN_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, UP_DOWN: IdleState, DOWN_DOWN: IdleState},
}

class Elf:

    def __init__(self):
        self.x, self.y = 128 * 4, 720 - 64
        self.stand0_image = load_image('image\\character_right_stand0.png')
        self.stand1_image = load_image('image\\character_right_stand1.png')
        self.width = 0
        self.high = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.look_vector = 1 #0부터 상하좌우
        self.time = get_time()

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        if self.y < 360:
            main_state.elf_move_window_y = 360 - self.y
        if self.x > 640 and self.x < 1920:
                main_state.elf_move_window_x = 640 - self.x

        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if get_time() >= self.time + 0.3:  # 화살발사
                if self.look_vector == 0:
                    elf_arrow = Elf_arrow(self.x, self.y, 0, 10)
                elif self.look_vector == 1:
                    elf_arrow = Elf_arrow(self.x, self.y, 0, -10)
                elif self.look_vector == 2:
                    elf_arrow = Elf_arrow(self.x, self.y, -10, 0)
                elif self.look_vector == 3:
                    elf_arrow = Elf_arrow(self.x, self.y, 10, 0)

                game_world.add_object(elf_arrow, 2)
                self.time = get_time()