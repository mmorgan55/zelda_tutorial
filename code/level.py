import pygame as pg
from settings import *
from tile import Tile
from player import Player
from debug import debug
from os.path import dirname, join
from support import *
from random import choice
from weapon import Weapon
from ui import UI

dir_name = dirname(__file__)


class Level:
    def __init__(self):
        # Get display surface
        self.display_surface = pg.display.get_surface()

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pg.sprite.Group()

        # Attack sprites
        self.current_attack = None

        # Player
        self.player = None

        # User interface
        self.ui = UI()

        # Sprite setup
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout(join(dir_name, '../map/map_FloorBlocks.csv')),
            'grass': import_csv_layout(join(dir_name, '../map/map_Grass.csv')),
            'object': import_csv_layout(join(dir_name, '../map/map_LargeObjects.csv'))

        }

        graphics = {
            'grass': import_folder(join(dir_name, '../graphics/grass')),
            'objects': import_folder(join(dir_name, '../graphics/objects'))
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        if style == 'boundary':
                            Tile((x, y), (self.obstacle_sprites,), 'invisible')
                        if style == 'grass':
                            random_grass_img = choice(graphics['grass'])
                            Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'grass', random_grass_img)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'grass', surf)

        self.player = Player((2000, 1430),
                             (self.visible_sprites,),
                             self.obstacle_sprites,
                             self.create_attack,
                             self.destroy_attack,
                             self.create_magic,
                             self.destroy_magic)

    def create_attack(self):
        self.current_attack = Weapon(self.player, (self.visible_sprites,))

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self, style, strength, cost):
        print(style)
        print(cost)
        print(strength)

    def destroy_magic(self):
        pass

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)


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
