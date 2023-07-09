"""Handles Control For Airplane and Simulates Function of Arduino Controller
-Incomplete"""
import pygame as pg
import numpy as np

class PlaneController:
    def __init__(self, waypoint, home_pos):
        self.user_input = False
        # Controller
        self.target = waypoint
        # Mode 0: go to target
        self.waypoint = waypoint
        # Mode 1: return to home
        self.home = home_pos
        self.gain = 1
        self.last_pos = home_pos
        self.d_target = self.target[0:1] - self.home[0:1]

    def get_command(self, pos, angle):
        ret = self.get_controller_input(pos, angle)
        self.last_pos = pos
        return ret

    def get_controller_input(self, pos, angle):
        self.d_target = self.target - pos
        self.t_theta = np.arctan2(-self.d_target[1], self.d_target[0])
        if np.sqrt(sum(self.d_target**2))<100:
            heading_error=0
        else:
            heading_error = self.determine_heading_error(angle)  # Angle in Radians
        ret = heading_error*self.gain
        lim = 1.5
        if abs(ret) > lim:
            ret = lim*ret/abs(ret)
        return ret  # Throttle and Control Surface Commands

    def set_target(self, mode):
        if mode == 0:
            self.target = self.waypoint
        elif mode == 1:
            self.target = self.home

    def determine_heading_error(self, theta):
        """Returns error in heading angle to the target position in radians(+ right, - left)"""
        # d_posxy = pos[0:2] - self.last_pos[0:2]
        # if d_posxy[0] == 0 and d_posxy[1] == 0:
        #     return 0
        if self.t_theta < 0:
            self.t_theta += 2*np.pi
        if theta < 0:
            theta += 2*np.pi
        anti_t = self.t_theta - np.pi
        if self.t_theta > theta > anti_t:
            # Left
            dtheta = self.t_theta - theta
        else:  # Right
            dtheta = self.t_theta-2*np.pi - theta
        return dtheta

