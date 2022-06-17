import pygame as pg
from settings import *


class Upgrade:
    def __init__(self, player):

        # General setup
        self.display_surface = pg.display.get_surface()
        self.player = player
        self.attribute_number = len(self.player.stats)
        self.attribute_names = list(self.player.stats.keys())
        self.font = pg.font.Font(UI_FONT, UI_FONT_SIZE)
        self.max_values = list(player.max_stats.values())

        # Item dimensions
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6

        # Selection system
        self.selection_index = 0
        self.selection_time = 0
        self.can_move = True
        self.item_list = []
        self.create_items()

    def input(self):
        keys = pg.key.get_pressed()

        if self.can_move:
            if keys[pg.K_RIGHT]:
                self.selection_index = (self.selection_index + 1) % self.attribute_number
                self.can_move = False
                self.selection_time = pg.time.get_ticks()
            elif keys[pg.K_LEFT]:
                self.selection_index = (self.selection_index - 1) % self.attribute_number
                self.can_move = False
                self.selection_time = pg.time.get_ticks()

            if keys[pg.K_SPACE]:
                self.can_move = False
                self.selection_time = pg.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        current_time = pg.time.get_ticks()
        if current_time - self.selection_time >= 300:
            self.can_move = True

    def create_items(self):
        for item, index in enumerate(range(self.attribute_number)):
            # Vertical position
            top = self.display_surface.get_size()[1] * 0.1

            # Horizontal position
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_number
            left = (item * increment) + (increment - self.width) // 2

            # Create the object
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def display(self):
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            # Get attributes
            name = self.attribute_names[index]
            value = self.player.get_current_stat_value(index)
            max_value = self.max_values[index]
            cost = self.player.get_stat_upgrade_cost(index)
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)


class Item:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pg.Rect(left, top, width, height)
        self.index = index
        self.font = font

    def display_names(self, surface, name, cost, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        # Attributes names for each box
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop=self.rect.midtop + pg.math.Vector2(0, 20))

        # Cost to upgrade each attribute
        cost_surf = self.font.render(f'{int(cost)}', False, color)
        cost_rect = cost_surf.get_rect(midbottom=self.rect.midbottom - pg.math.Vector2(0, 20))

        # Draw onto surface
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected):
        top = self.rect.midtop + pg.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pg.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pg.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        pg.draw.line(surface, color, top, bottom, 5)
        pg.draw.rect(surface, color, value_rect)

    def trigger(self, player):
        upgrade_attribute = list(player.stats.keys())[self.index]

        if player.exp >= player.upgrade_cost[upgrade_attribute] and \
                player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            player.exp -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            player.upgrade_cost[upgrade_attribute] *= 1.4

        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display(self, surface, selection_num, name, value, max_value, cost):
        if self.index == selection_num:
            pg.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pg.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pg.draw.rect(surface, UI_BG_COLOR, self.rect)
            pg.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, name, cost, self.index == selection_num)
        self.display_bar(surface, value, max_value, self.index == selection_num)
