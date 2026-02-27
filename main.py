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

time_between_fruits=1000
last_spawn_fruit=pygame.time.get_ticks()


spawn_Fruits(750,fruits, width, heigth, screen)
spawn_Individuals(50, individuals, width, heigth, screen)

fonte = pygame.font.SysFont('Arial', 30)

mortos=0
qtd_individuos_inicial=len(individuals)

perceptors=[]
energized=[]
velociters=[]
socialists=[]
ragers=[]

while running:
    qtd_individuos=len(individuals)
    mortos=str(qtd_individuos_inicial-qtd_individuos)

    deaths_text = fonte.render(mortos, True, (255,255,255))

    #Event Tracker
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)
    grid_draw(width, heigth, square_size, grid_color, screen)

    current_time=pygame.time.get_ticks()

    if current_time-last_spawn_fruit>time_between_fruits:
        spawn_Fruits(50, fruits, width, heigth, screen)
        for individual in individuals:
            print(individual.energy)

        last_spawn_fruit=current_time

    for individual in individuals:
        individual.draw_Individual()
        flee(individual, individuals)
        ready_to_reproduce(individual)
        find_mate(individual, individuals)
        hunt(individual, fruits, individuals)

        movement(individual)

    new_born=[]

    for individual in individuals:
        if individual.ready_to_reproduce and individual.mate_target:
            if(checking_Collision(individual, individual.mate_target)):
                reproduction_cost=50
                individual.energy-=reproduction_cost
                individual.mate_target.energy -= reproduction_cost

                new_genes = mix_genes(individual, individual.mate_target)
                individual.ready_to_reproduce=False
                individual.mate_target.ready_to_reproduce=False
                individual.mate_target=None

                child=Individual(new_genes[0],
                                 new_genes[1],
                                 new_genes[2],
                                 new_genes[3],
                                 new_genes[4],
                                 individual.pos.x,
                                 individual.pos.y,
                                 individual.screen)
                
                new_born.append(child)

    individuals.extend(new_born)

    for fruit in fruits:
        fruit.draw_Fruit()

    for individual in individuals:
        for fruit in fruits[:]:
            if checking_Collision(individual, fruit):
                energy_to_receive=fruit.protein*10
                individual.energy+=energy_to_receive

                if individual.most_significant_gene==3:
                    for friend in individuals:
                        if friend!=individual and friend.most_significant_gene==3:
                            if individual.pos.distance_to(friend.pos)<=individual.perception:
                                friend.energy+=(energy_to_receive)

                fruits.remove(fruit)

        attack(individual, individuals)

    checking_Death(individuals)
    

    screen.blit(deaths_text,(100, 100))

    clock.tick(60)
    pygame.display.flip()
pygame.quit()
sys.exit()
