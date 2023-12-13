import pygame as pg
import math
from pygame.math import Vector2


class Projectile(pg.sprite.Sprite):
    def __init__(self, pos, offset):
        super().__init__()
        mouse_pos = pg.mouse.get_pos()
        self.start_pos = Vector2(pos)

        direction = Vector2(mouse_pos) + offset - self.start_pos
        self.direction = direction.normalize()
        angle = (180 / math.pi) * - math.atan2(direction.y, direction.x) - 180

        image = pg.image.load('assets/weapons/dagger.png').convert_alpha()
        image = pg.transform.scale(image, (54, 18))
        self.image = pg.transform.rotate(image, angle)
        self.rect = self.image.get_rect(center=pos)

        self.speed = 15
        self.hit_damage = 15
        self.distance_alive = 200

    def update(self):
        delta_pos = self.direction * self.speed
        self.rect.x += delta_pos.x
        self.rect.y += delta_pos.y

        dist = self.start_pos.distance_to(Vector2((self.rect.x, self.rect.y)))
        if dist >= self.distance_alive:
            self.kill()

    def render(self, screen, offset):
        offset_pos = self.rect.topleft - offset
        screen.blit(self.image, offset_pos)



