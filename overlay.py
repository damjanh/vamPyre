import pygame as pg

from settings import WINDOW_SIZE


class Overlay:
    def __init__(self, overlay_close):
        color = pg.Color(64, 64, 64)
        self.surface = pg.Surface(WINDOW_SIZE)
        self.surface.fill(color)
        self.surface.set_alpha(128)
        self.rect = self.surface.get_rect()
        self.overlay_close_callback = overlay_close

    def render(self, screen):
        screen.blit(self.surface, self.rect)

    def close_overlay(self):
        self.overlay_close_callback()
