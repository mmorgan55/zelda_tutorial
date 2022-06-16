import pygame as pg
from os.path import dirname, join

dir_name = dirname(__file__)


class Weapon(pg.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0]

        # Graphic
        full_path = join(dir_name, f'../graphics/weapons/{player.weapons[player.weapon_index]}/{direction}.png')
        self.image = pg.image.load(full_path).convert_alpha()

        # Weapon placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pg.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pg.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pg.math.Vector2(-10, 0))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pg.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(center=player.rect.center)
