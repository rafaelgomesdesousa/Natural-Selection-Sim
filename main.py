import pygame
import sys
from objects import *
from functions import *
import random
from simulation import *

pygame.init()

width=1200
heigth=800
screen=pygame.display.set_mode((1200,800))
pygame.display.set_caption("Natural Selection")

while True:

    choice=display_initial_screen(screen, width, heigth)

    if choice=="create":
        play_simulation(screen, width, heigth, mode="create")

    elif choice=="predefined":
        play_simulation(screen,width, heigth, mode="predefined")

    elif choice=="statistics":
        print("Still working")


