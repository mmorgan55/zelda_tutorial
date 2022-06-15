import pygame as pg
from settings import *
from entity import Entity
from os.path import dirname, join
from support import import_folder

dir_name = dirname(__file__)


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups):
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # Graphics setup
        self.animations = None
        self.import_enemy_assets(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

    def import_enemy_assets(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = join(dir_name, f'../graphics/monsters/{name}/')
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)