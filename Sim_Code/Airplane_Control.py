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
        self.max_climb_aoa = .2 # Rad
        p_throttle = 1
        self.p_aileron = .1
        self.p_elevon = .1
        self.p_tail = .1

        # Heading Error Transfer Functions
        self.tf_h_r = lambda theta: theta * 15/180
        self.tf_h_y = lambda theta: theta
        self.tf_h_p = lambda theta: abs(theta) * 10/180
        self.tf_h_th = lambda theta: abs(theta) * .3/np.pi * p_throttle
        # Pitch Error Transfer Functions
        self.tf_p_th = lambda theta: theta * .3/np.pi * p_throttle

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
        self.d_target = self.target[0:2] - pos[0:2]
        self.t_theta = np.arctan2(self.d_target[1], self.d_target[0])

        heading_error = self.determine_heading_error(pos, angle)  # Angle in Radians
        aoa_target = self.determine_pitch_target(pos)

        throttle = self.throttle_cruise + self.tf_h_th(heading_error) + self.tf_p_th(aoa_target)
        if throttle > 1:
            throttle = 1

        roll_error = self.tf_h_r(heading_error) - angle[0]
        roll = roll_error * self.p_aileron

        pitch_error = self.tf_h_p(heading_error) + aoa_target - angle[1]
        pitch = pitch_error * self.p_elevon

        yaw_error = self.tf_h_y(self.t_theta) - angle[2]
        yaw = yaw_error * self.p_tail
        return throttle, roll, pitch, yaw  # Throttle and Control Surface Commands

    def set_target(self):
        if self.mode == 0:
            self.target = self.waypoints[self.current_point, :]
        elif self.mode == 1:
            self.target = self.home

    def determine_heading_error(self, pos, angles):
        """Returns error in heading angle to the target position in radians(+ right, - left)"""
        # d_posxy = pos[0:2] - self.last_pos[0:2]
        # if d_posxy[0] == 0 and d_posxy[1] == 0:
        #     return 0
        theta = np.arctan2(np.sin(angles[2])*np.cos(angles[1]), np.cos(angles[2])*np.cos(angles[1]))  # atan(Y, X)
        if self.t_theta < 0:
            self.t_theta += 2*np.pi
        anti_t = self.t_theta - np.pi
        if self.t_theta > theta > anti_t:
            # Left
            dtheta = self.t_theta - theta
        else:  # Right
            dtheta = self.t_theta-2*np.pi - theta
        return dtheta

    def determine_pitch_target(self, pos):
        alt = pos[2]
        d_alt = self.target[2] - alt
        t_pitch = d_alt/10 * np.pi/180
        if abs(t_pitch) > self.max_climb_aoa:
            t_pitch = t_pitch/abs(t_pitch) * self.max_climb_aoa
        return t_pitch
