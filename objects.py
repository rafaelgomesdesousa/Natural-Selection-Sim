import math
import pygame
import random

class Individual:
    def __init__(self, p, e, v, s, a, x, y, screen):
        self.perception=p*50
        self.energy=e*50
        self.velocity=0.5+v/2 #MUDAR PRA 5 DEPOIS
        self.sociability=s
        self.angriness=a
        self.initial_energy = self.energy
        self.pos=pygame.math.Vector2(x, y)
        self.size=5+self.angriness
        self.genes=[p,e,v,s,a]
        self.most_significant_gene=self.genes.index(max(self.genes))
        self.color=(255,255,255)
        self.screen=screen
        self.carnivore=False
        self.direction=pygame.math.Vector2(0,0)
        self.time_change=0
        self.damage=0
        self.injured=False

        self.energy_waist=0.05

        self.alvo=None
        self.predator=None

        self.ready_to_reproduce=False
        self.mate_target=None

        self.skills=[]
        self.check_evolution()

        if(self.most_significant_gene==4):
            self.carnivore=True

        if self.carnivore:
            self.damage=50
            #self.energy_waist=0.03
            self.velocity+=0.18

        if self.most_significant_gene==1:
            self.energy_waist=0.01

        if self.most_significant_gene==2:
            self.energy_waist=0.5

        #Setting Color
        if self.most_significant_gene==4:
            self.color='red'
        elif self.most_significant_gene==3:
            self.color='green'
        elif self.most_significant_gene==2:
            self.color='purple'
        elif self.most_significant_gene==1:
            self.color='yellow'
        elif self.most_significant_gene==0:
            self.color='blue'

    
    def check_evolution(self):
        if self.genes[2]>=7:
            branch=random.choice(["Sprint", "Endurance"])
            self.skills.append(branch)

        if self.genes[3]>=7:
            branch=random.choice(["Leadership", "Socialism"])
            self.skills.append(branch)

        if self.genes[4]>=7:
            branch=random.choice(["Killer", "Energy_Steal"])
            self.skills.append(branch)

            if "Killer" in self.skills:
                self.damage=self.damage*2
                self.velocity=self.velocity+0.5
        

    #Desenhar individuo
    def draw_Individual(self):
        #pygame.draw.circle(self.screen, self.color, self.pos, self.size)
        pygame.draw.rect(self.screen, self.color, (self.pos.x, self.pos.y, self.size, self.size))

        #if self.ready_to_reproduce:
            #pygame.draw.circle(self.screen, (255, 105, 180), self.pos, self.perception, 1)
        if "Leadership" in self.skills:
            pygame.draw.rect(self.screen, (255, 215, 0), (self.pos.x - 2, self.pos.y - 2, self.size + 4, self.size + 4), 2)

        elif "Socialism" in self.skills:
            pygame.draw.rect(self.screen, (0, 255, 255), (self.pos.x - 2, self.pos.y - 2, self.size + 4, self.size + 4), 2)

        if "Killer" in self.skills:
            pygame.draw.rect(self.screen, (255, 255, 255), (self.pos.x - 2, self.pos.y - 2, self.size + 4, self.size + 4), 2)

        if "Energy_Steal" in self.skills:
            pygame.draw.rect(self.screen, (148, 0, 211), (self.pos.x - 2, self.pos.y - 2, self.size + 4, self.size + 4), 2)

        




class Fruits:
    def __init__(self, protein, x, y, screen):
        self.protein=protein
        self.pos=pygame.math.Vector2(x,y)
        self.size=2
        self.screen=screen
        
        self.color=('white')


    def draw_Fruit(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.size)

