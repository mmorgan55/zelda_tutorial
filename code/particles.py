import pygame as pg
from support import import_folder
from os.path import dirname, join
from random import  choice

dir_name = dirname(__file__)


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # Magic particles
            'flame': import_folder(join(dir_name, '../graphics/particles/flame/frames')),
            'aura': import_folder(join(dir_name, '../graphics/particles/aura')),
            'heal': import_folder(join(dir_name, '../graphics/particles/heal/frames')),

            # Attack particles
            'claw': import_folder(join(dir_name, '../graphics/particles/claw')),
            'slash': import_folder(join(dir_name, '../graphics/particles/slash')),
            'sparkle': import_folder(join(dir_name, '../graphics/particles/sparkle')),
            'leaf_attack': import_folder(join(dir_name, '../graphics/particles/leaf_attack')),
            'thunder': import_folder(join(dir_name, '../graphics/particles/thunder')),

            # Monster death particles
            'squid': import_folder(join(dir_name, '../graphics/particles/smoke_orange')),
            'raccoon': import_folder(join(dir_name, '../graphics/particles/raccoon')),
            'spirit': import_folder(join(dir_name, '../graphics/particles/nova')),
            'bamboo': import_folder(join(dir_name, '../graphics/particles/bamboo')),

            # Leaf particles
            'leaf': (
                import_folder(join(dir_name, '../graphics/particles/leaf1')),
                import_folder(join(dir_name, '../graphics/particles/leaf2')),
                import_folder(join(dir_name, '../graphics/particles/leaf3')),
                import_folder(join(dir_name, '../graphics/particles/leaf4')),
                import_folder(join(dir_name, '../graphics/particles/leaf5')),
                import_folder(join(dir_name, '../graphics/particles/leaf6')),
                self.reflect_images(import_folder(join(dir_name, '../graphics/particles/leaf1'))),
                self.reflect_images(import_folder(join(dir_name, '../graphics/particles/leaf2'))),
                self.reflect_images(import_folder(join(dir_name, '../graphics/particles/leaf3'))),
                self.reflect_images(import_folder(join(dir_name, '../graphics/particles/leaf4'))),
                self.reflect_images(import_folder(join(dir_name, '../graphics/particles/leaf5'))),
                self.reflect_images(import_folder(join(dir_name, '../graphics/particles/leaf6')))
            )

        }

    def reflect_images(self, frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pg.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pg.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
