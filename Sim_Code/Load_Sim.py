"""Loads the Outside Data and Parameters needed to make the Sim including:
- List of Waypoints
- A Display Range based on those Waypoints for X and Y vals based on GPS coordinates -> Position on screen in function
? An Image to use for the background that is of the display area based on satellite or height map of coordinates
"""
import numpy as np

class SimData:
    def __init__(self):
        self.waypoints = np.array(((.4, .5, 40),
                                   (.4, 100, 50),
                                  (50, -300, 50)))
