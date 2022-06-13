import pygame as pg
from settings import *
from os.path import dirname, join

dir_name = dirname(__file__)


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pg.image.load(join(dir_name, '../graphics/test/rock.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
