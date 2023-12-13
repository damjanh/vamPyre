import pygame as pg

from overlay import Overlay
from player_upgrades import PlayerUpgrades, PlayerUpgradeType

from settings import WINDOW_SIZE

UPGRADE_DIMENSIONS = (100, 100)
UPGRADES_MARGIN = 10


class Button(pg.sprite.Sprite):
    def __init__(self, image, rect, position):
        super().__init__()
        self.image = image
        self.rect = rect
        self.position = position


class LevelUpOverlay(Overlay):
    def __init__(self, font, overlay_close, apply_upgrade):
        super().__init__(overlay_close)
        self.font = font
        self.apply_upgrade_callback = apply_upgrade
        self.button_collision_idx = -1
        self.click = False
        self.player_upgrades = PlayerUpgrades()
        self.button_group = pg.sprite.Group()
        self.available_upgrades = self.player_upgrades.player_upgrades_per_level_dict.get(1)
        self.construct_menu()

    def set_player_new_level(self, level):
        self.available_upgrades = self.player_upgrades.player_upgrades_per_level_dict.get(level)
        self.construct_menu()

    def construct_menu(self):
        size = len(self.available_upgrades)
        x_start = WINDOW_SIZE[0] / 2 - (size * UPGRADE_DIMENSIONS[0]) / 2

        for idx, upgrade in enumerate(self.available_upgrades):
            surface = pg.Surface(UPGRADE_DIMENSIONS)
            if upgrade.type == PlayerUpgradeType.HEALTH:
                surface.fill('green')
            elif upgrade.type == PlayerUpgradeType.ATTACK_DMG:
                surface.fill('red')
            elif upgrade.type == PlayerUpgradeType.SPEED:
                surface.fill('blue')
            else:
                surface.fill('yellow')

            rect = surface.get_rect()
            rect.centery = WINDOW_SIZE[1] / 2
            rect.x = x_start

            self.button_group.add(Button(surface, rect, idx))
            x_start = rect.x + UPGRADE_DIMENSIONS[1] + UPGRADES_MARGIN * 2

    def update(self):
        self.click = pg.mouse.get_pressed()[0]

        mx, my = pg.mouse.get_pos()

        for button in self.button_group:
            if button.rect.collidepoint((mx, my)):
                self.button_collision_idx = button.position
                if self.click:
                    self.click = False
                    self.apply_upgrade_callback(self.available_upgrades[button.position])
                    super().close_overlay()

    def render(self, screen):
        super().render(screen)

        for button in self.button_group:
            screen.blit(button.image, button.rect)
