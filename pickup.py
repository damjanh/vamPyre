import pygame as pg

from enum import Enum


class PickupType(Enum):
    EXP = 1,
    HEALTH = 2


class Pickup(pg.sprite.Sprite):
    def __init__(self, pos, image, p_type: PickupType):
        super().__init__()
        self.image = image
        self.p_type = p_type
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        pass

    def render(self, screen, offset):
        offset_pos = self.rect.topleft - offset
        screen.blit(self.image, offset_pos)
