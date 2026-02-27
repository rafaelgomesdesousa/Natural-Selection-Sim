import pygame
import math
from objects import *
import random


# Desenhar Grid

def grid_draw(width, heigth, grid_size, grid_color, screen):
    for x in range(0, width, grid_size):
        pygame.draw.line(screen, grid_color, (x, 0), (x, heigth))

    for y in range(0, heigth, grid_size):
        pygame.draw.line(screen, grid_color, (0, y), (width, y))

# Spawnar objetos aleatorios

#Frutas:

def spawn_Fruits(fruits_qtd, fruits, width, heigth,screen):
    for i in range(0,fruits_qtd):
        random_protein=random.randint(1,3)
        random_x=random.randint(0, width)
        random_y=random.randint(0,heigth)
        fruits.append(Fruits(random_protein, random_x, random_y, screen))

#Individuos

def spawn_Individuals(individuals_qtd, individuals, width, heigth, screen):
    for i in range(0, individuals_qtd):

        points=[5,3,2,1,1]

        random.shuffle(points)

        p,e,v,s,a=points

        x=random.randint(0,width)
        y=random.randint(0,heigth)

        individuals.append(Individual(p, e, v, s, a, x, y, screen))


def hunt(individual, fruits, individuals):
    entities=fruits+individuals
    best=None
    closest=float('inf')

    individual.alvo = None

    if individual.carnivore:
        for alvo in individuals:
            if alvo==individual or alvo.carnivore:
                continue

            dist_x=alvo.pos.x-individual.pos.x
            dist_y=alvo.pos.y-individual.pos.y

            distance=math.hypot(dist_x,dist_y)

            if distance<individual.perception and distance<closest:
                closest=distance
                best=alvo
            
    else:
        for alvo in fruits:
            if alvo==individual:
                continue

            dist_x=alvo.pos.x-individual.pos.x
            dist_y=alvo.pos.y-individual.pos.y

            distance=math.hypot(dist_x,dist_y)

            if distance<individual.perception and distance<closest:
                closest=distance
                best=alvo
            
    if best is not None:
        individual.alvo=best


def movement(individual):
    if individual.alvo:
        direction=pygame.math.Vector2(individual.alvo.pos.x,individual.alvo.pos.y)-individual.pos

        if direction.length()>0:

            direction=direction.normalize()
            individual.pos+=direction*individual.velocity

    else:
        individual.time_change-=1

        if individual.time_change<=0:
            random_x=random.randint(-1,1)
            random_y=random.randint(-1,1)
            individual.direction=pygame.math.Vector2(random_x,random_y)

            if individual.direction.length()>0:
                individual.direction=individual.direction.normalize()

            individual.time_change=random.randint(20,60)
        
        if hasattr(individual, 'direction'):
            individual.pos += individual.direction * individual.velocity

        #individual.pos.x = individual.pos.x
        #individual.pos.y = individual.pos.y

    individual.pos.x = max(0, min(individual.pos.x, individual.screen.get_width()))
    individual.pos.y = max(0, min(individual.pos.y, individual.screen.get_height()))
        #individual.pos.x, individual.pos.y = individual.pos.x, individual.pos.y
    
    energy_cost=0.1
    speed_energy = individual.velocity * 0.02

    total_spent=energy_cost+speed_energy

    individual.energy-=total_spent


#Verificando Colisao

def checking_Collision(obj_1,obj_2):
    distance=pygame.math.Vector2(obj_1.pos).distance_to(obj_2.pos)

    if distance<(obj_1.size+obj_2.size):
        return True
    return False


def checking_Death(list_individuals):
    for individual in list_individuals[:]:
        if individual.energy<=0:
            list_individuals.remove(individual)

def attack(individual, list_individuals):
    if individual.carnivore:
        for i in list_individuals:
            if i==individual:
                continue

            if not i.carnivore:
                if checking_Collision(individual, i):
                    i.energy-=individual.damage
                    individual.energy+=10

                    if not i.injured:
                        i.velocity+=0.5
                        i.injured=True


