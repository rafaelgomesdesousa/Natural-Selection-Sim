import pygame
import sys
from objects import *
from functions import *
import random

pygame.init()

width=1200
heigth=800
screen=pygame.display.set_mode((1200,800))
pygame.display.set_caption("Natural Selection")
clock=pygame.time.Clock()
running=True

#Criando Grid
square_size=50

background_color=(0,0,0)
grid_color=(255,255,255)

adam=Individual(2,2,3,4,5,width/2, heigth/2, screen)
eva=Individual(1,1,4,5,2, width/2+10, heigth/2+10, screen)

individuals=[]
fruits=[]

time_between_fruits=2000
last_spawn_fruit=pygame.time.get_ticks()


spawn_Fruits(100,fruits, width, heigth, screen)
spawn_Individuals(100, individuals, width, heigth, screen)

while running:

    #Event Tracker
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)
    grid_draw(width, heigth, square_size, grid_color, screen)

    current_time=pygame.time.get_ticks()

    if current_time-last_spawn_fruit>time_between_fruits:
        spawn_Fruits(3, fruits, width, heigth, screen)

        last_spawn_fruit=current_time

    for individual in individuals:
        individual.draw_Individual()
        hunt(individual, fruits, individuals)
        movement(individual)

    for fruit in fruits:
        fruit.draw_Fruit()

    for individual in individuals:
        for fruit in fruits[:]:
            if checking_Collision(individual, fruit):
                individual.energy+=fruit.protein*10
                fruits.remove(fruit)

        attack(individual, individuals)

    checking_Death(individuals)


    clock.tick(60)
    pygame.display.flip()
pygame.quit()
sys.exit()
