import pygame as pg
from os.path import dirname, join

dir_name = dirname(__file__)


class Player(pg.sprite.Sprite):
    def __init__(self, pos, groups, obstacles):
        super().__init__(groups)
        self.image = pg.image.load(join(dir_name, '../graphics/test/player.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # Player actions
        self.direction = pg.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacles = obstacles

    def input(self):
        keys = pg.key.get_pressed()

        # Movement input
        if keys[pg.K_UP]:
            self.direction.y = -1
        elif keys[pg.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pg.K_LEFT]:
            self.direction.x = -1
        elif keys[pg.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        # Attack input
        if keys[pg.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pg.time.get_ticks()

        # Magic input
        if keys[pg.K_LSHIFT] and not self.attacking:
            self.attacking = True
            self.attack_time = pg.time.get_ticks()

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

    def update(self):
        self.input()
        self.cooldowns()
        self.move(self.speed)
