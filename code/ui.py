import pygame as pg
from settings import *
from os.path import dirname, join

dir_name = dirname(__file__)


class UI:
    def __init__(self):
        # General
        self.display_surface = pg.display.get_surface()
        self.font = pg.font.Font(UI_FONT, UI_FONT_SIZE)

        # Bar setup
        self.health_bar_rect = pg.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pg.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # Weapons
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pg.image.load(join(dir_name, path))
            self.weapon_graphics.append(weapon)

    def show_bar(self, current, max_amount, bg_rect, color):
        pg.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # Converting stat to pixel length
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        pg.draw.rect(self.display_surface, color, current_rect)
        pg.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))
        pg.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pg.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def selection_box(self, left, top, has_switched):
        bg_rect = pg.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pg.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pg.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pg.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect)

        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        weapon_surf = self.weapon_graphics[weapon_index]
        bg_rect = self.selection_box(10, 630, has_switched)  # Weapon
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def display(self, player):
        # Display health/energy bars
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        # Display player experience
        self.show_exp(player.exp)

        # Display current weapon and magic player has equipped
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        # self.selection_box(80, 635)
