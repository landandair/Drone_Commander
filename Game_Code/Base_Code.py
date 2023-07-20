from pygame import sprite
import pygame as pg
import numpy as np
import Pygame_Tools as tools

class Base(sprite.Sprite):
    """Simulate Flight Characteristics and control system for autopilot"""
    def __init__(self, pos, health=20, zoom=1):
        """Inputs:
        - pos: base center point
        - health: number of hits to destroy it
        - zoom: zoom level of map
        """
        super().__init__()
        image = pg.image.load('Assets/Plane.png')
        self.image = pg.transform.scale(image, np.array(image.get_size())*zoom)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.health = health

    def kill(self):
        if self.health <= 0:
            # Prob nice to add death animation
            for group in self.groups():
                group.remove(self)
            self.groups().clear()
        self.health -= 1
