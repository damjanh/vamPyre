import pygame as pg
import random


class ParticleFire:
    def __init__(self, pos):
        self.pos = pos
        self.particles = []
        self.colors = [(255, 0, 0), (255, 215, 0), (255, 69, 0)]

    def update(self, pos):
        for x in range(random.randint(15, 25)):
            particle = Particle(
                pos[0],
                pos[1],
                random.randint(0, 20) / 10, random.randint(-3, -1),
                random.randint(2, 5), random.choice(self.colors)
            )
            self.particles.append(particle)

    def emit(self, screen, offset):
        for particle in self.particles:
            particle.render(screen)
            if particle.radius <= 0:
                self.particles.remove(particle)

    def destroy(self):
        self.particles.clear()


class Particle:
    def __init__(self, x, y, xvel, yvel, radius, color, gravity=None):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.radius = radius
        self.color = color
        self.gravity = gravity

    def render(self, screen):
        self.x += self.xvel
        self.y += self.yvel
        if self.gravity is not None:
            self.yvel += self.gravity
        self.radius -= 0.1

        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)
