import pygame as pg
from settings import *
from tile import Tile
from player import Player
from os.path import dirname, join
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer

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
        self.attack_sprites = pg.sprite.Group()
        self.attackable_sprites = pg.sprite.Group()

        # Player
        self.player = None

        # Particles
        self.animation_player = AnimationPlayer()

        # User interface
        self.ui = UI()

        # Sprite setup
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout(join(dir_name, '../map/map_FloorBlocks.csv')),
            'grass': import_csv_layout(join(dir_name, '../map/map_Grass.csv')),
            'object': import_csv_layout(join(dir_name, '../map/map_LargeObjects.csv')),
            'entities': import_csv_layout(join(dir_name, '../map/map_Entities.csv'))
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
                            Tile((x, y),
                                 (self.visible_sprites, self.obstacle_sprites, self.attackable_sprites),
                                 'grass', random_grass_img)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'grass', surf)
                        if style == 'entities':
                            if col == '394':
                                self.player = Player((x, y),
                                                     (self.visible_sprites,),
                                                     self.obstacle_sprites,
                                                     self.create_attack,
                                                     self.destroy_attack,
                                                     self.create_magic,
                                                     self.destroy_magic)
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Enemy(monster_name, (x, y),
                                      (self.visible_sprites, self.attackable_sprites),
                                      self.obstacle_sprites,
                                      self.damage_player)

    def create_attack(self):
        self.current_attack = Weapon(self.player, (self.visible_sprites, self.attack_sprites))

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

    def player_attack(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pg.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pg.math.Vector2(0, 60)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, (self.visible_sprites,))
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pg.time.get_ticks()

            # TODO: add particles when hit

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.update_enemy(self.player)
        self.player_attack()
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

    def update_enemy(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
