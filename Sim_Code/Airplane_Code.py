"""Holds Code for dealing with the plane vector and converting between the reference and aircraft frame of reference"""
from pygame import sprite
import pygame as pg

class FakePlane(sprite.Sprite):
    def __init__(self, start_pos):
        super().__init__()
        self.og_image = pg.image.load('Assets/Plane.png')
        self.image = self.og_image
        self.rect = self.image.get_rect()
        self.rect.center = start_pos



    def update(self):
        self.do_physics()
        self.update_pos()

    def do_physics(self):
        pass

    def update_pos(self):
        pass
