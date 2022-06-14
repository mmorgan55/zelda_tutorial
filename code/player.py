import pygame as pg
from os.path import dirname, join
from support import import_folder
from settings import weapon_data

dir_name = dirname(__file__)


class Player(pg.sprite.Sprite):
    def __init__(self, pos, groups, obstacles, create_attack, destroy_attack):
        super().__init__(groups)
        self.image = pg.image.load(join(dir_name, '../graphics/test/player.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # Graphics/animations setup
        self.animations = None
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        # Player actions
        self.direction = pg.math.Vector2()
        self.speed = 5
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

            # Switch weapons

            if keys[pg.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pg.time.get_ticks()
                self.weapon_index = (self.weapon_index + 1) % len(self.weapons)
                self.current_weapon = self.weapons[self.weapon_index]

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

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.check_collisions('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.check_collisions('vertical')
        self.rect.center = self.hitbox.center

    def check_collisions(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacles:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # Moving left
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # Moving right
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacles:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # Moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # Moving  up
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pg.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed

        if self.frame_index > len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
