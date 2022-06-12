import pygame as pg
from os.path import dirname, join

dir_name = dirname(__file__)


class Player(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pg.image.load(join(dir_name, '../graphics/test/player.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pg.math.Vector2()
        self.speed = 5

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

        self.rect.center += self.direction * speed

    def update(self):
        self.input()
        self.move(self.speed)
