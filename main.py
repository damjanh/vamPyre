import sys
import pygame as pg
import pygame.freetype

from settings import WINDOW_SIZE
from main_menu import MainMenu
from game import Game


class Main:
    def __init__(self):
        pg.init()
        pg.font.init()
        self.font = pg.freetype.Font('assets/font/Plain_Germanica.ttf', 28)

        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.clock = pg.time.Clock()

        self.main_menu = MainMenu(self.screen, self.clock, self.font, self.start_game, self.quit)
        self.game = None

    def start_game(self):
        self.game = Game(self.screen, self.clock, self.font, self.end_game, self.quit)
        self.game.run()

    def end_game(self):
        self.main_menu = MainMenu(self.screen, self.clock, self.font, self.start_game, self.quit)
        self.main_menu.run()

    def quit(self):
        pg.quit()
        sys.exit()

    def run(self):
        self.main_menu.run()


if __name__ == '__main__':
    main = Main()
    main.run()
