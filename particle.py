import pygame as pg
import random


class Particle:
    def __init__(self, pos, num, color='red'):
        self.particles = []
        self.color = color
        for i in range(num):
            self.add_particles(pos)

    def update(self, pos):
        pass

    def emit(self, screen, offset):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][1] += particle[2][0]
                particle[0][0] += particle[2][1]
                particle[1] -= 0.2
                offset_pos = pg.Vector2(particle[0][0], particle[0][1]) - offset
                pg.draw.circle(screen, pg.Color(self.color), offset_pos, int(particle[1]))

    def add_particles(self, pos):
        pos_x, pos_y = pos
        radius = 10
        direction_x = random.randint(-3, 3)
        direction_y = random.randint(-3, 3)
        particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
        self.particles.append(particle_circle)

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy
