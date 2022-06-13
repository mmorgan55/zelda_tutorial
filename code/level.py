import pygame as pg
from settings import *
from tile import Tile
from player import Player
from debug import debug
from os.path import dirname, join
from support import import_csv_layout

dir_name = dirname(__file__)


class Level:
    def __init__(self):
        # Get display surface
        self.display_surface = pg.display.get_surface()

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pg.sprite.Group()

        self.player = None

        # Sprite setup
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout(join(dir_name, '../map/map_FloorBlocks.csv'))
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
        self.player = Player((2000, 1500), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()

        # General
        self.display_surface = pg.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] / 2
        self.half_height = self.display_surface.get_size()[1] / 2
        self.offset = pg.math.Vector2(100, 200)

        # Creating the floor
        self.floor_surf = pg.image.load(join(dir_name, '../graphics/tilemap/ground.png')).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # Getting offset for the player camera
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
