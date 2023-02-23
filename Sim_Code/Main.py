"""Jonathan Huwaldt, 2023
Main Start to the Simulation
- Loads Data and determines background range and scale
? Open Menu
- Starts Main Sim Window
? Save Data after running
"""
import pygame as pg
import Load_Sim
import Sim_Window

def main():
    print('starting')
    pg.init()
    pg.font.init()
    data = Load_Sim.SimData()
    window = Sim_Window.MainWindow(data)

    while True:
        window.update()


if __name__ == '__main__':
    main()