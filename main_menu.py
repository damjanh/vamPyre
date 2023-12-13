import pygame as pg

from pygame.freetype import Font

from settings import WINDOW_SIZE


class MainMenu:
    def __init__(self, screen, clock, font: Font, callback_start, callback_quit):
        self.screen = screen
        self.clock = clock
        self.font = font
        self.callback_start = callback_start
        self.callback_quit = callback_quit

        self.title_surface = pg.transform.scale(pg.image.load('assets/menu/title.png').convert(), WINDOW_SIZE)

        self.button_play = pg.Rect(200, 100, 200, 50)
        self.button_quit = pg.Rect(200, 180, 200, 50)

        self.click = False
        self.mouse_over_play = False
        self.mouse_over_quit = False

    def draw_text(self, text, color, pos):
        self.font.render_to(self.screen, pos, text, color)

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.callback_quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.callback_quit()
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.click = True
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    self.click = False

            self.screen.fill('purple')

            self.update()

            self.render()

            pg.display.flip()
            self.clock.tick(60)

    def update(self):
        mx, my = pg.mouse.get_pos()
        if self.button_play.collidepoint((mx, my)):
            self.mouse_over_play = True
            self.mouse_over_quit = False
            if self.click:
                self.click = False
                self.callback_start()
        elif self.button_quit.collidepoint((mx, my)):
            self.mouse_over_play = False
            self.mouse_over_quit = True
            if self.click:
                self.click = False
                self.callback_quit()
        else:
            self.mouse_over_play = False
            self.mouse_over_quit = False

    def render(self):
        self.screen.blit(self.title_surface, (0, 0))
        if self.mouse_over_play:
            color = pg.Color('gray')
        else:
            color = pg.Color('white')
        pg.draw.rect(self.screen, color, self.button_play)

        if self.mouse_over_quit:
            color = pg.Color('gray')
        else:
            color = pg.Color('white')
        pg.draw.rect(self.screen, color, self.button_quit)

        self.draw_text('Play', pg.Color('black'), self.button_play.topleft)
        self.draw_text('Quit', pg.Color('black'), self.button_quit.topleft)
