"""Holds Code that handles the content of the window as well as containing all of the pygame sprite groups needed
for the sim"""
from Airplane_Code import Plane
from Airplane_Control import PlaneController
import pygame as pg
import Pygame_Tools as Tool
import sys
import numpy as np


class MainWindow:
    def __init__(self):
        self.zoom = .5
        # Screen Setup
        self.h_w = 9/16  # height to width Ratio
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

        # Objects
        self.obj_dict = {}
        self.obj_array = np.array(())
        self.plane_list = []
        self.planes = pg.sprite.Group()
        self.fort_beac = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.bombs = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        # Load values for first level
        self.load_from_file('file')
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

    def load_from_file(self, file_name):
        # [type, hop, x, y, closest x, closest y]
        self.obj_dict = {}
        self.plane_list = []
        self.planes = pg.sprite.Group()
        self.fort_beac = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.bombs = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        self.obj_array = np.array(((1, 90, 100, 100, 500, 500),
                                   (1, 90, 200, 100, 500, 500),
                                   (1, 90, 300, 100, 500, 500),
                                   (1, 90, 400, 100, 500, 500)),
                                  dtype=float)
        for i, row in enumerate(self.obj_array):
            if row[0] == 1:
                controller = PlaneController(row[4:], row[2:4])
                obj = Plane(self.monitor_size, controller, zoom=self.zoom)
                self.planes.add(obj)
                self.plane_list.append(obj)
            else:
                controller = PlaneController(row[4:], row[2:4])
                obj = Plane(self.monitor_size, controller, zoom=self.zoom)
                self.planes.add(obj)
                self.plane_list.append(obj)
            self.obj_dict[obj] = i

    def remove_obj(self, obj):
        index = self.obj_dict[obj]
        for key in self.obj_dict:
            if self.obj_dict[key]>index:
                self.obj_dict[key] -= 1

        self.plane_list.remove(obj)
        self.obj_dict.pop(obj)
        self.obj_array = np.delete(self.obj_array, index)
        print(self.obj_dict)
        obj.kill()
