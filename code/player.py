import pygame as pg
from os.path import dirname, join

dir_name = dirname(__file__)


class Player(pg.sprite.Sprite):
    def __init__(self, pos, groups, obstacles):
        super().__init__(groups)
        self.image = pg.image.load(join(dir_name, '../graphics/test/player.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pg.math.Vector2()
        self.speed = 5

        self.obstacles = obstacles

    def input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_UP]:
            self.direction.y = -1
        elif keys[pg.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pg.K_LEFT]:
            self.direction.x = -1
        elif keys[pg.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed
        self.check_collisions('horizontal')
        self.rect.y += self.direction.y * speed
        self.check_collisions('vertical')

    def check_collisions(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacles:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:  # Moving left
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:  # Moving right
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacles:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:  # Moving down
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:  # Moving  up
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.input()
        self.move(self.speed)
