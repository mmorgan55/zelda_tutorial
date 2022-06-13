import pygame as pg
from settings import *
from os.path import dirname, join

dir_name = dirname(__file__)


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pg.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
