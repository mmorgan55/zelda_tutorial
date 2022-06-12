import pygame as pg
from settings import *
from tile import Tile
from player import Player
from debug import debug


class Level:
    def __init__(self):
        # Get display surface
        self.display_surface = pg.display.get_surface()

        # Sprite group setup
        self.visible_sprites = pg.sprite.Group()
        self.obstacle_sprites = pg.sprite.Group()

        self.player = None

        # Sprite setup
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites])

    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
        debug(self.player.direction)
