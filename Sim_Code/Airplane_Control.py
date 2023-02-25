"""Handles Control For Airplane and Simulates Function of Arduino Controller
-Incomplete"""
import pygame as pg
import numpy as np

class PlaneController:
    def __init__(self, waypoints, home_pos):
        self.user_input = False
        self.mode = 0  # Mode 0(waypoints), Mode 1(RTH), Mode 2(Loiter)
        # Controller
        # Mode 0
        self.waypoints = waypoints
        self.current_point = 0
        self.target = waypoints[self.current_point, :]
        # Mode 1
        self.home = home_pos
        # Gains
        self.throttle_cruise = .5
        self.p_throttle = 1
        self.p_aileron = 1
        self.p_elevon = 1
        self.p_tail = 1

        # Heading Error Transfer Functions
        self.tf_h_r = lambda theta: theta * 15/180
        self.tf_h_y = lambda theta: theta
        self.tf_h_p = lambda theta: abs(theta) * 10/180
        self.tf_h_th = lambda theta: abs(theta) * .3/np.pi
        # Pitch Error Transfer Functions
        self.tf_h_th = lambda theta: theta * .3/np.pi

        self.last_pos = home_pos
        self.d_target = self.target[0:1] - self.home[0:1]

    def get_command(self, pos, angles):
        if self.user_input:
            ret = self.get_user_input()
        else:
            ret = self.get_controller_input(pos, angles)
        self.last_pos = pos
        return ret

    def get_user_input(self):
        pg.key.get_pressed()
        throttle = 0
        aileron = 0
        elevon = 0
        vert = 0
        return throttle, aileron, elevon, vert

    def get_controller_input(self, pos, angle):
        self.set_target()
        self.d_target = self.target[0:1] - self.home[0:1]
        heading_error = self.determine_heading_error(pos)  # Angle in Radians

        throttle = 0
        aileron = 0
        elevon = 0
        vert = 0
        return throttle, aileron, elevon, vert

    def set_target(self):
        if self.mode == 0:
            self.target = self.waypoints[self.current_point, :]
        elif self.mode == 1:
            self.target = self.home

    def determine_heading_error(self, pos):
        """Returns error in heading angle to the target position in radians(+ right, - left)"""
        d_posxy = pos[0:1] - self.last_pos[0:1]
        theta = np.arctan2(d_posxy[1], d_posxy[0])  # atan(Y, X)
        if theta < 0:
            theta += 2*np.pi
        t_theta = np.arctan2(self.d_target[1], self.d_target[0])
        if t_theta < 0:
            t_theta += 2*np.pi
        left = t_theta - theta
        if left < 0:
            left += 2*np.pi
        if left < np.pi:
            return -left  # Turn Left(- Angle)
        else:
            return 2*np.pi-left  # Turn Right(+ Angle)
