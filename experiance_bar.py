import pygame as pg

from settings import WINDOW_SIZE


class ExperienceBar:
    def __init__(self, size=(200, 20), progress=0):
        self.border_color = (255, 255, 255)
        self.bar_color = pg.Color('black')
        self.bar_inner_color = pg.Color('purple')

        pos_y = WINDOW_SIZE[1] - 40
        pos_x = WINDOW_SIZE[0] / 2 - 100

        self.progress = progress
        self.pos = (pos_x, pos_y)
        self.size = size

    def update(self, progress):
        self.progress = progress

    def render(self, screen):
        inner_pos = (self.pos[0] + 3, self.pos[1] + 3)
        inner_size = ((self.size[0] - 6) * self.progress, self.size[1] - 6)
        pg.draw.rect(screen, self.bar_color, (*self.pos, *self.size), 1)
        pg.draw.rect(screen, self.bar_inner_color, (*inner_pos, *inner_size))
