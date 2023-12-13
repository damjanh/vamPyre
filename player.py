import pygame as pg
from health_bar import draw_health_bar
from player_upgrades import PlayerUpgrade, PlayerUpgradeType


class Player(pg.sprite.Sprite):
    def __init__(self, pos, player_shoot, bounds, player_died, player_level_up):
        super().__init__()

        self.player_exp_required_dict = {
            0: 0,
            1: 100,
            2: 300,
            3: 600,
            4: 1000,
            5: 1500,
            6: 2100,
            7: 2800,
            8: 3600,
            9: 4500,
            10: 6000
        }

        image = pg.image.load('assets/characters/player.png').convert_alpha()
        self.image = pg.transform.scale(image, (75, 75))
        self.rect = self.image.get_rect(center=pos)
        self.bounds = bounds

        self.player_shoot = player_shoot
        self.player_died = player_died
        self.player_level_up = player_level_up

        self.speed = 5.0
        self.left = True

        self.max_health = 30
        self.health = 30

        self.reload_time = 500
        self.last_shot_time = 0

        self.exp = 0
        self.level = 1
        self.required_exp = self.player_exp_required_dict.get(self.level)

        self.applied_upgrades = []

    def shoot(self):
        if pg.time.get_ticks() > self.last_shot_time + self.reload_time:
            self.last_shot_time = pg.time.get_ticks()
            self.player_shoot(self.rect.center)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            # TODO: player death animation
            self.kill()
            self.player_died()

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def apply_upgrade(self, upgrade: PlayerUpgrade):
        if upgrade.type == PlayerUpgradeType.HEALTH:
            self.max_health += upgrade.amount
        elif upgrade.type == PlayerUpgradeType.ATTACK_DMG:
            # TODO: Projectile damage
            return
        elif upgrade.type == PlayerUpgradeType.ATTACK_SPD:
            self.reload_time -= upgrade.amount
        elif upgrade.type == PlayerUpgradeType.SPEED:
            self.speed += upgrade.amount

        self.applied_upgrades.append(upgrade)

    def experience(self, amount):
        self.exp += amount
        if self.level < 10:
            while self.required_exp <= self.exp:
                self.level += 1
                self.required_exp = self.player_exp_required_dict.get(self.level)
                self.exp = 0
                self.player_level_up()

    def get_experience_percentage(self):
        if self.level == 10:
            return 1
        return self.exp / self.required_exp

    def get_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            if self.bounds['right'] > self.rect.right:
                self.rect.x += self.speed
            self.check_flip('right')
            self.left = False
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            if self.bounds['left'] < self.rect.left:
                self.rect.x -= self.speed
            self.check_flip('left')
            self.left = True
        if keys[pg.K_UP] or keys[pg.K_w]:
            if self.bounds['top'] < self.rect.top:
                self.rect.y -= self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            if self.bounds['bottom'] > self.rect.bottom:
                self.rect.y += self.speed

        if pg.mouse.get_pressed()[0]:
            self.shoot()

    def check_flip(self, direction):
        if (direction == 'left' and not self.left) or (direction == 'right' and self.left):
            self.image = pg.transform.flip(self.image, flip_y=False, flip_x=True)

    def update(self):
        self.get_input()

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

