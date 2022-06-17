import pygame as pg
from settings import *
from random import randint


class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('heal', player.rect.center + pg.math.Vector2(0, -60), groups)
            self.animation_player.create_particles('aura', player.rect.center, groups)

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost

            if player.status.split('_')[0] == 'right':
                direction = pg.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left':
                direction = pg.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up':
                direction = pg.math.Vector2(0, -1)
            else:
                direction = pg.math.Vector2(0, 1)

            for i in range(1, 6):
                if direction.x:  # Flames going Horizontal
                    offset_x = (direction.x * i) * TILE_SIZE
                    x = player.rect.centerx + offset_x + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    y = player.rect.centery + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)
                else:  # Flame going vertical
                    offset_y = (direction.y * i) * TILE_SIZE
                    x = player.rect.centerx + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)
