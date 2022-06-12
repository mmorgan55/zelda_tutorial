import sys

import pygame as pg
from settings import *

class Game:
    def __init__(self):

        # General setup
        pg.init()
        self.screen = pg.display.set_mode((0,0))
        self.clock = pg.time.Clock()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.screen.fill('grey')
            pg.display.update()
            self.clock.tick(60)

if __name__ == 'main':
    game = Game()
    game.run()
