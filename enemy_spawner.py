import pygame as pg
import random

from enemy import Enemy

MAX_ENEMIES = 15
ENEMY_SPAWN_EVENT = pg.USEREVENT + 1


class EnemySpawner:
    def __init__(self, bounds, camera_rect):
        self.enemy_asset_dict = {
            'grub_1': pg.transform.scale(pg.image.load('assets/enemy/enemy_grub1.png').convert_alpha(), (50, 50)),
            'grub_2': pg.transform.scale(pg.image.load('assets/enemy/enemy_grub2.png').convert_alpha(), (50, 50)),
        }

        self.bounds = bounds
        self.camera_rect = camera_rect

        pg.time.set_timer(ENEMY_SPAWN_EVENT, 1000)

        self.enemies_group = pg.sprite.Group()

    def spawn_new_enemy(self):
        if len(self.enemies_group) < MAX_ENEMIES:
            position_x = random.randint(self.bounds['left'], self.bounds['right'])
            position_y = random.randint(self.bounds['top'], self.bounds['bottom'])
            enemy_asset_key = random.choice([
                'grub_1',
                'grub_2']
            )
            image = self.enemy_asset_dict.get(enemy_asset_key)
            self.enemies_group.add(Enemy((position_x, position_y), image))

    def update(self, player_pos):
        for enemy in self.enemies_group:
            enemy.update(player_pos)

    def render(self, screen, offset):
        for enemy in self.enemies_group.sprites():
            enemy.render(screen, offset)
