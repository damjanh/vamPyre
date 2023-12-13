
import pygame as pg

from settings import WINDOW_SIZE
from level_up_overlay import LevelUpOverlay
from map import Map
from player import Player
from pickup import PickupType
from pickup_spawner import PickupSpawner
from projectile import Projectile
from particle import Particle
from particle_fire import ParticleFire
from enemy_spawner import EnemySpawner, ENEMY_SPAWN_EVENT
from experiance_bar import ExperienceBar


class Game:
    def __init__(self, screen, clock, font, callback_end_game, callback_quit):
        self.isRunning = True
        self.screen = screen
        self.clock = clock
        self.font = font
        self.callback_end_game = callback_end_game
        self.callback_quit = callback_quit
        self.start_time = 0

        self.overlay_active = False
        self.overlay_start_time = 0
        self.overlay_total_time = 0

        # Camera offset
        self.offset = pg.math.Vector2()
        self.half_w = self.screen.get_size()[0] // 2
        self.half_h = self.screen.get_size()[1] // 2

        # Box setup
        self.camera_borders = {'left': 400, 'right': 400, 'top': 200, 'bottom': 200}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.screen.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.screen.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pg.Rect(l, t, w, h)

        self.map = Map()
        self.experience_bar = ExperienceBar()
        self.player = Player(
            (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2),
            self.player_shoot,
            self.map.player_bounds,
            self.player_died,
            self.player_level_up
        )
        self.overlay = LevelUpOverlay(self.font, self.overlay_close, self.player.apply_upgrade)
        self.enemy_spawner = EnemySpawner(self.map.player_bounds, self.camera_borders)
        self.pickup_spawner = PickupSpawner()
        self.player_group = pg.sprite.GroupSingle(self.player)

        self.projectiles_group = pg.sprite.Group()

        self.particles = []
        self.particles.append(
            ParticleFire((300, 300))
        )

    def box_target_camera(self, target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def player_shoot(self, player_pos):
        self.projectiles_group.add(Projectile(player_pos, self.offset))

    def player_died(self):
        self.isRunning = False

    def player_level_up(self):
        self.overlay_active = True
        self.overlay_start_time = pg.time.get_ticks()

    def overlay_close(self):
        self.overlay_active = False
        self.overlay_total_time += self.overlay_start_time - pg.time.get_ticks()

    def run(self):
        self.start_time = pg.time.get_ticks()
        while self.isRunning:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.callback_quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.isRunning = False
                if event.type == ENEMY_SPAWN_EVENT and not self.overlay_active:
                    self.enemy_spawner.spawn_new_enemy()

            self.screen.fill('black')

            self.update()

            self.render()

            pg.display.flip()
            self.clock.tick(60)

        self.callback_end_game()

    def update(self):
        if self.overlay_active:
            self.overlay.update()
            return

        self.player.update()

        self.enemy_spawner.update(self.player.rect)
        self.pickup_spawner.update()

        for particle in self.particles:
            particle.update((300, 300))

        for projectile in self.projectiles_group.sprites():
            projectile.update()

        self.check_collisions_player_with_enemies()
        self.check_collision_projectiles_with_enemies()
        self.check_collision_pickups_with_player()

        self.experience_bar.update(self.player.get_experience_percentage())

        # TODO: have enemies to feed the vampire and give it heals - by Misel

    def check_collisions_player_with_enemies(self):
        enemies_hit = pg.sprite.spritecollide(self.player_group.sprite, self.enemy_spawner.enemies_group, False)
        if enemies_hit:
            for enemy in enemies_hit:
                self.player.take_damage(enemy.attack_damage)
                self.particles.append(Particle(self.player.rect.center, 20))
                enemy.kill()
                self.particles.append(Particle(enemy.rect.center, 20, color='purple'))

    def check_collision_projectiles_with_enemies(self):
        for projectile in self.projectiles_group.sprites():
            enemies_hit = pg.sprite.spritecollide(projectile, self.enemy_spawner.enemies_group, False)
            if enemies_hit:
                projectile.kill()
                for enemy in enemies_hit:
                    if enemy.damage_check_kill(projectile.hit_damage):
                        self.particles.append(Particle(enemy.rect.center, 20, color='purple'))
                        self.pickup_spawner.spawn_crystal(enemy.rect.center)

    def check_collision_pickups_with_player(self):
        if self.player_group:
            pickups_hit = pg.sprite.spritecollide(self.player_group.sprite, self.pickup_spawner.pickup_group, True)
            if pickups_hit:
                for pickup in pickups_hit:
                    if pickup.p_type == PickupType.HEALTH:
                        self.player.heal(10)
                    elif pickup.p_type == PickupType.EXP:
                        self.player.experience(10)
                        pass

    def render(self):
        self.map.render(self.screen, self.offset)
        self.box_target_camera(self.player)

        self.pickup_spawner.render(self.screen, self.offset)
        self.enemy_spawner.render(self.screen, self.offset)

        self.player.render(self.screen, self.offset)

        for projectile in self.projectiles_group.sprites():
            projectile.render(self.screen, self.offset)

        for particle in self.particles:
            particle.emit(self.screen, self.offset)

        # TODO: Remove particle when spent

        offset_pos = self.camera_rect.topleft - self.offset

        #pg.draw.rect(self.screen, 'yellow', pg.Rect((offset_pos.x, offset_pos.y), (self.screen.get_size()[0] - self.camera_borders['right'] * 2, self.screen.get_size()[1] - self.camera_borders['bottom'] * 2)), 1)

        self.experience_bar.render(self.screen)

        if self.overlay_active:
            self.overlay.render(self.screen)
        else:
            self.render_game_time()

    def render_game_time(self):
        time_s = (pg.time.get_ticks() - self.start_time - self.overlay_total_time) // 1000
        time_m = time_s // 60
        time_s = time_s - time_m * 60
        if time_m < 10:
            time_m = f'0{time_m}'
        if time_s < 10:
            time_s = f'0{time_s}'

        self.font.render_to(self.screen, (20, 20), f'{time_m}:{time_s}', 'black')
