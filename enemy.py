import pygame as pg
from health_bar import draw_health_bar


class Enemy(pg.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

        self.speed = 1.0
        self.left = True

        self.max_health = 30
        self.health = 30
        self.attack_damage = 3

    def damage_check_kill(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return True
        return False

    def check_flip(self, direction):
        if (direction == 'left' and not self.left) or (direction == 'right' and self.left):
            self.image = pg.transform.flip(self.image, flip_y=False, flip_x=True)

    def update(self, player_rect):
        if player_rect.x > self.rect.x:
            self.check_flip('right')
            self.left = False
        else:
            self.check_flip('left')
            self.left = True

        if player_rect.x > self.rect.x:
            self.rect.x += self.speed
        elif player_rect.x < self.rect.x:
            self.rect.x -= self.speed

        if player_rect.y > self.rect.y:
            self.rect.y += self.speed
        elif player_rect.y < self.rect.y:
            self.rect.y -= self.speed

    def render(self, screen, offset):
        offset_pos = self.rect.topleft - offset
        screen.blit(self.image, offset_pos)
        self.draw_health(screen, offset)

    def draw_health(self, surf, offset: pg.Vector2):
        health_rect = pg.Rect(0, 0, self.image.get_width(), 7)
        health_rect.midbottom = self.rect.centerx, self.rect.top
        offset_pos = health_rect.topleft - offset
        draw_health_bar(surf, offset_pos, health_rect.size,
                        (0, 0, 0), (255, 0, 0), (0, 255, 0), self.health / self.max_health)
