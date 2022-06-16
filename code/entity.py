import pygame as pg
from math import sin


class Entity(pg.sprite.Sprite):
    def __init__(self, groups, obstacles):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pg.math.Vector2(0, 0)
        self.hitbox = None
        self.obstacles = obstacles

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.check_collisions('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.check_collisions('vertical')
        self.rect.center = self.hitbox.center

    def check_collisions(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacles:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # Moving left
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # Moving right
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacles:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # Moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # Moving  up
                        self.hitbox.top = sprite.hitbox.bottom

    def flicker_entity(self):
        value = sin(pg.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
