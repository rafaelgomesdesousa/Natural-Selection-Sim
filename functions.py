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
        random_protein=random.randint(1,2)
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

def flee(individual, individuals):

    if individual.carnivore:
        individual.predator=None
        return

    worst=None
    closest=float('inf')

    individual.predator=None

    for i in individuals:
        if i==individual or not i.carnivore:
            continue
        dist_x=i.pos.x-individual.pos.x
        dist_y=i.pos.y-individual.pos.y

        distance=math.hypot(dist_x,dist_y)

        if distance<individual.perception and distance<closest:
            closest=distance
            worst=i

    if worst is not None:
        individual.predator=worst


def movement(individual):

    if individual.predator:
        direction=individual.pos-pygame.math.Vector2(individual.predator.pos.x, individual.predator.pos.y)

        if direction.length()>0:
            direction = direction.normalize()
            individual.pos += direction * individual.velocity

    elif individual.mate_target:
        direction=pygame.math.Vector2(individual.mate_target.pos-individual.pos)

        if direction.length()>0:
            direction=direction.normalize()
            individual.pos+=direction*individual.velocity

    elif individual.alvo:
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
    
    energy_cost=individual.energy_waist   #COLOCARA 0.05 DEPOIS
    #speed_energy = individual.velocity * 0.05  #COLOCAR 0.02 DEPOIS

    total_spent=energy_cost

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

def ready_to_reproduce(individual):
    if individual.energy>individual.initial_energy+300:
        individual.ready_to_reproduce=True


def find_mate(individual, individuals):
    individual.mate_target = None

    if not individual.ready_to_reproduce:
        return
    
    best_mate = None
    closest = float('inf')

    for i in individuals:
        if individual==i:
            continue
            
        if i.ready_to_reproduce and individual.most_significant_gene==i.most_significant_gene:

            distance=individual.pos.distance_to(i.pos)

            if distance<individual.perception and distance<closest:
                closest = distance
                best_mate = i
    if best_mate is not None:
        individual.mate_target = best_mate


def mix_genes(father, mother):
    son_genes=[]
    mutation_rate=0.25

    for i in range(5):
        chosen_gene=random.choice([father.genes[i], mother.genes[i]])

        if random.random()<mutation_rate:
            mutation=random.choice([1,-1])
            chosen_gene+=mutation

            chosen_gene=max(1, chosen_gene)

        son_genes.append(chosen_gene)

    return son_genes

def find_group(individual, individuals):
    if individual.most_significant_gene!=3:
        return
    
    if individual.predator or individual.mate_target or individual.alvo:
        return 

    closest_friend=None
    closest=float('inf')

    for i in individuals:
        if individual==i:
            continue
        if i.most_significant_gene==3:
            distance = individual.pos.distance_to(i.pos)

            if 15 < distance < individual.perception and distance < closest:
                closest = distance
                closest_friend = i

    if closest_friend:
        direction=closest_friend.pos-individual.pos
        if direction.length()>0:
            direction = direction.normalize()

            individual.pos += direction * (individual.velocity * 0.8)
