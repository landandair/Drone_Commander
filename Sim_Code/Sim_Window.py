"""Holds Code that handles the content of the window as well as containing all of the pygame sprite groups needed
for the sim"""
from Airplane_Code import FakePlane
from Airplane_Control import PlaneController
import pygame as pg
import Pygame_Tools as Tool
import sys
import numpy as np


class MainWindow:
    def __init__(self):
        waypoint = np.array((.5, .5))
        # Screen Setup
        self.h_w = 9/16  # height to width Ratio
        pg.display.init()
        self.monitor_size = np.array((pg.display.Info().current_w, pg.display.Info().current_h))

        if self.monitor_size[0] * self.h_w > self.monitor_size[1]:
            self.w = self.monitor_size[1]/self.h_w
        else:
            self.w = self.monitor_size[0]
        self.h = self.w * self.h_w

        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        # Turns 0-1 cords into pixel cords
        self.f_real_xy = lambda xy: np.array((xy[0]*self.w + (self.monitor_size[0]-self.w),
                                            xy[1]*self.h + (self.monitor_size[1]-self.h)))
        # Sprite Groups
        self.background = pg.sprite.Group()
        back = Tool.Background(pg.image.load('Assets/Background1.png'), self.w, self.h)
        back.rect.center = self.monitor_size/2
        self.background.add(back)

        self.planes = pg.sprite.Group()
        controller = PlaneController(self.f_real_xy(waypoint), self.f_real_xy(np.array((.1, .1))))
        plane = FakePlane(self.monitor_size, controller)
        self.planes.add(plane)
        # Misc Vars
        self.clock = pg.time.Clock()
        self.pause = False
        self.quit = False

    def update(self):
        self.manage_events()
        if self.quit:
            return

        if not self.pause and self.clock.get_fps():
            dt = 1/self.clock.get_fps()
            self.planes.update(dt)
        else:
            dt = 0

        self.screen.fill('Black')
        self.background.draw(self.screen)
        self.draw_lines()
        self.planes.draw(self.screen)
        pg.display.flip()
        self.clock.tick(120)

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
                if event.key == pg.K_p:
                    self.pause = not self.pause

    def draw_lines(self):
        line_color = (100, 0, 0)
        for plane in self.planes:
            if plane.has_signal:
                pg.draw.line(self.screen, line_color, plane.controller.target, plane.controller.last_pos, width=4)




