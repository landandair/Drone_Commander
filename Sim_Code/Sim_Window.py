"""Holds Code that handles the content of the window as well as containing all of the pygame sprite groups needed
for the sim"""
import pygame as pg
import Pygame_Tools as Tool
import sys
import numpy as np


class MainWindow:
    def __init__(self, data):
        self.data = data
        # Screen Setup
        self.h_w = 9/16  # height to width Ratio
        pg.display.init()
        self.monitor_size = np.array((pg.display.Info().current_w, pg.display.Info().current_h))
        if self.monitor_size[0] * self.h_w > self.monitor_size[1]:
            self.w = self.monitor_size[1]/self.h_w
        else:
            self.w = self.monitor_size[0]
        self.screen = pg.display.set_mode([0,0], pg.FULLSCREEN)
        # Sprite Groups
        self.background = pg.sprite.Group()
        back = Tool.Background(pg.image.load('Assets/Background1.png'), self.w,
                               self.h_w*self.w)
        back.rect.center = self.monitor_size/2
        self.background.add(back)

        # Misc Vars
        self.clock = pg.time.Clock()
        self.quit = False

    def update(self):
        self.manage_events()
        if self.quit:
            return

        self.background.draw(self.screen)
        pg.display.flip()
        self.clock.tick(60)

    def manage_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit = True
                    pg.quit()
                    sys.exit()



