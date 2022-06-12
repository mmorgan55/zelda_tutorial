import pygame as pg
from os.path import dirname, join

dir_name = dirname(__file__)


class Player(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pg.image.load('/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
