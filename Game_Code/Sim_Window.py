"""Holds Code that handles the content of the window as well as containing all of the pygame sprite groups needed
for the sim"""
import Pygame_Tools as tools
from Base_Code import Base
from Airplane_Code import Plane
from Airplane_Control import PlaneController
import pygame as pg
import Pygame_Tools as Tool
from range_vis_calc import update_ranges
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
        self.range = self.f_real_xy([.2, 0])[0] * self.zoom
        # Sprite Groups
        self.background = pg.sprite.Group()
        back = Tool.Background(pg.image.load('Assets/Background1.png'), self.w, self.h)
        back.rect.center = self.monitor_size/2
        self.background.add(back)

        # Objects
        self.obj_dict = {}
        self.obj_array = np.array(())
        self.plane_list = []
        # Things with health or controls
        self.planes = pg.sprite.Group()
        self.ground_forces = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        # Bullets
        self.bullets = pg.sprite.Group()
        self.bombs = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        # Ui
        self.ui_elements = pg.sprite.Group()
        # Load values for first level
        self.load_from_file('file')
        self.obj_array = update_ranges(self.obj_array, self.range)
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
            self.planes.update(dt, self.obj_dict, self.obj_array)
            self.enemies.update(dt, self.obj_dict, self.obj_array)
            self.obj_array = update_ranges(self.obj_array, self.range)
            self.ground_forces.update()
            # Bullets
            self.bullets.update(dt)
            self.bombs.update(dt)
            self.explosions.update(dt)
        else:
            dt = 0
        self.ui_elements.update()
        # display layer from bottom to top
        self.screen.fill('Black')
        self.background.draw(self.screen)
        self.draw_lines()
        self.bullets.draw(self.screen)
        self.enemies.draw(self.screen)
        self.ground_forces.draw(self.screen)
        self.ui_elements.draw(self.screen)
        self.bombs.draw(self.screen)
        self.explosions.draw(self.screen)
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
        self.obj_array = np.array(((0, 0, 100, 100, 500, 500, 0),
                                   (2, 0, 200, 100, 500, 500, np.pi/2),
                                   (2, 0, 300, 100, 500, 500, 0),
                                   (2, 0, 600, 100, 500, 500, 0)),
                                  dtype=float)
        for i, row in enumerate(self.obj_array):
            if row[0] == 0:
                obj = Base(np.array(row[2:4]), zoom=self.zoom)
                health_bar = tools.HealthBar(np.array(row[2:4])+np.array((0, 40*self.zoom)), obj, width=80, height=5)
                self.ground_forces.add(obj)
                self.ui_elements.add(health_bar)
            elif row[0] == 2:
                controller = PlaneController(np.array(row[4:6]), np.array(row[2:4]))
                obj = Plane(self.monitor_size, controller, row[6], zoom=self.zoom)
                self.planes.add(obj)
                self.plane_list.append(obj)
            else:
                controller = PlaneController(np.array(row[4:6]), np.array(row[2:4]))
                obj = Plane(self.monitor_size, controller, row[6], zoom=self.zoom)
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
        obj.kill()
