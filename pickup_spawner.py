import pygame as pg

from pickup import Pickup, PickupType


class PickupSpawner:
    def __init__(self):
        self.pickup_asset_dict = {
            'potion_health': pg.transform.scale(pg.image.load('assets/pickup/potion_red.png').convert_alpha(), (25, 25)),
            'potion_health_big': pg.transform.scale(pg.image.load('assets/pickup/potion_big_red.png').convert_alpha(), (25, 25)),
            'crystal_blue': pg.transform.scale(pg.image.load('assets/pickup/crystal_blue.png').convert_alpha(), (25, 25)),
        }

        self.pickup_group = pg.sprite.Group()

    def spawn_potion(self, pos):
        self.pickup_group.add(Pickup(pos, self.pickup_asset_dict.get('potion_health'), PickupType.HEALTH))

    def spawn_crystal(self, pos):
        self.pickup_group.add(Pickup(pos, self.pickup_asset_dict.get('crystal_blue'), PickupType.EXP))

    def update(self):
        pass

    def render(self, screen, offset):
        for pickup in self.pickup_group.sprites():
            pickup.render(screen, offset)
