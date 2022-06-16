import pygame as pg
from os.path import dirname, join
from support import import_folder
from settings import weapon_data, magic_data
from entity import Entity

dir_name = dirname(__file__)


class Player(Entity):
    def __init__(self, pos, groups, obstacles, create_attack, destroy_attack, create_magic, destroy_magic):
        super().__init__(groups, obstacles)
        self.image = pg.image.load(join(dir_name, '../graphics/test/player.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # Graphics/animations setup
        self.animations = None
        self.import_player_assets()
        self.status = 'down'

        # Player actions
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # Player weapons
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapons = list(weapon_data.keys())
        self.current_weapon = self.weapons[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # Player magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())
        self.current_magic = self.magic[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # Player stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.exp = 123

        self.obstacles = obstacles

    def import_player_assets(self):
        character_path = join(dir_name, '../graphics/player/')
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
            'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []
        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pg.key.get_pressed()
        if not self.attacking:

            # Movement input
            if keys[pg.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pg.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pg.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pg.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            # Attack input
            if keys[pg.K_SPACE]:
                self.attacking = True
                self.attack_time = pg.time.get_ticks()
                self.create_attack()

            # Magic input
            if keys[pg.K_LSHIFT]:
                self.attacking = True
                self.attack_time = pg.time.get_ticks()
                style = self.magic[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)

            # Switch weapons
            if keys[pg.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pg.time.get_ticks()
                self.weapon_index = (self.weapon_index + 1) % len(self.weapons)
                self.current_weapon = self.weapons[self.weapon_index]

            if keys[pg.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pg.time.get_ticks()
                self.magic_index = (self.magic_index + 1) % len(self.magic)
                self.current_magic = self.magic[self.magic_index]

    def get_status(self):

        # Idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in self.status and 'attack' not in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0

            if 'attack' not in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def cooldowns(self):
        current_time = pg.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.current_weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

    def animate_player(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index > len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.current_weapon]['damage']
        print(base_damage + weapon_damage)
        return base_damage + weapon_damage

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate_player()
        self.move(self.speed)
