"""Holds Code for dealing with the plane vector and converting between the reference and aircraft frame of reference"""
from pygame import sprite
import pygame as pg
import Pygame_Tools as Tools
import numpy as np
from Airplane_Control import PlaneController


class Plane(sprite.Sprite):
    """Simulate Flight Characteristics and control system for autopilot"""

    def __init__(self, screen_size, Controller: PlaneController, zoom=1):
        """Inputs:
        - Start_Pos[Home Point in Meters(x,y)]
        - f_trans[Transfer Function f(x,y) Between meter cords and pixel Cords]
        - Controller Object which Gives Deflection Angles and throttle to be fed into the plane"""
        super().__init__()
        self.dt = 1/60
        self.has_signal = True
        # Disp Params
        self.og_image = pg.image.load('Assets/Plane.png')
        self.og_image = pg.transform.scale(self.og_image, np.array(self.og_image.get_size())*zoom)
        self.image = self.og_image
        self.rect = self.image.get_rect()
        self.rect.center = Controller.home
        self.screen_size = screen_size
        # Flight Characteristics(scuffed)
        self.speed = .02 * screen_size[0] * zoom  # pixels/sec
        self.theta = 0.  # Yaw angle
        self.plane_velocity = np.array((self.speed, 0.))
        self.pos = Controller.home
        # Controller
        self.controller = Controller
        Tools.rot(self)

    def update(self, dt):
        """Main Update Loop, Runs Every Frame
        - Get Controls
        - Do Physics Calculation
        - Update Position to Image"""
        self.dt = dt
        self.get_controls()
        self.do_physics()
        self.update_pos()

    def get_controls(self):
        """Gets control inputs from controller
        - Get Control from player/controller
        - Apply Controls to Plane"""
        d_theta = self.controller.get_command(self.pos, self.theta)
        self.theta += d_theta*self.dt
        if self.theta >= 2*np.pi:
            self.theta -= 2*np.pi
        elif self.theta < 0:
            self.theta += 2*np.pi

    def do_physics(self):
        """Handles Physics increments"""
        self.plane_velocity[0] = np.cos(self.theta) * self.speed
        self.plane_velocity[1] = -np.sin(self.theta) * self.speed
        self.pos += self.plane_velocity * self.dt

    def update_pos(self):
        self.rect.center = self.pos
        if self.has_signal:
            Tools.rot(self)
        else:
            self.image = pg.transform.scale(self.og_image, (0, 0))


