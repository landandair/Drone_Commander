import pygame
import numpy as np

# THE MAIN ROTATE FUNCTION
def rot(self):
    self.angle = self.theta*180/np.pi % 360
    self.image = pygame.transform.rotate(self.og_image, self.angle)
    self.rect = self.image.get_rect(center=self.rect.center)


# Basic Button
class Button(pygame.sprite.Sprite):
    """Basic button which doesn't handle collision or events and only acts as an image which can be scaled"""
    def __init__(self, pos, image, scale):
        super().__init__()
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.center = pos


class TextReadout(pygame.sprite.Sprite):
    """Makes a text line which takes in a center position, string or convertible number, and font object and prints it
    to the screen as a sprite object"""
    def __init__(self, pos, text, font='freesansbold.ttf', size=20,  centered=True):
        super().__init__()
        pygame.font.init()
        self.pos = pos
        self.image = font.render(str(text), True, 'white')
        self.rect = self.image.get_rect()
        self.centered = centered
        if centered:
            self.rect.center = pos
        else:
            self.rect.topleft = pos
        self.font = pygame.font.Font(font, size)

    def add_text(self, new_text):
        pygame.font.init()
        self.image = self.font.render(str(new_text), True, 'white')
        self.rect = self.image.get_rect()
        if self.centered:
            self.rect.center = self.pos
        else:
            self.rect.topleft = self.pos


class HealthBar(pygame.sprite.Sprite):
    """Makes a basic health bar which takes the 'health' attribute of a sprite
    and makes a health bar to those proportions"""
    def __init__(self, pos, ref_sprite, width=200, height=20):
        super().__init__()
        self.image = pygame.surface.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.ref = ref_sprite
        self.ratio = width/self.ref.health

    def update(self):
        self.rect.width = self.ref.health*self.ratio
        self.image = pygame.transform.scale(self.image, self.rect.size)
        self.image.fill('red')
        if self.ref.health <= 0:
            self.kill()


class Background(pygame.sprite.Sprite):
    def __init__(self, image, width, height):
        super().__init__()
        self.image = pygame.transform.scale(image, (int(width), int(height))).convert()
        self.rect = self.image.get_rect()


class KeyData:
    def __init__(self, id):
        """Class which holds all of the data that is needed to be sent across and back acrooss the network to
        facilitate multiplayer play
            -ship_pos: {} with key (id) and data
                [pos <vector>, vel <vector>, heading <float>, health <int>, animation state <int>, target<vector>, status <str>]
            -new_weapons: [] with contents of [type <str>, launcher <int>]
            -id: int player # of the ship controlled by the player"""
        # Format id: [pos vector, vel vector, theta, health, state, target_pos, ready]
        self.ships_pos = {}
        self.new_weapons = []
        self.id = id
