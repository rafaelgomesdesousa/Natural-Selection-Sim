import math
import pygame

class Individual:
    def __init__(self, p, e, v, s, a, x, y, screen):
        self.perception=p*50
        self.energy=e*50
        self.velocity=v/2
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

        self.alvo=None
        self.predator=None

        self.ready_to_reproduce=False
        self.mate_target=None

        if(self.angriness>=5):
            self.carnivore=True

        if self.carnivore:
            self.damage=50

        #Setting Color
        if self.most_significant_gene==4:
            self.color='red'
        elif self.most_significant_gene==3:
            self.color='yellow'
        elif self.most_significant_gene==2:
            self.color='purple'
        elif self.most_significant_gene==1:
            self.color='green'
        elif self.most_significant_gene==0:
            self.color='blue'

    #Desenhar individuo
    def draw_Individual(self):
        #pygame.draw.circle(self.screen, self.color, self.pos, self.size)
        pygame.draw.rect(self.screen, self.color, (self.pos.x, self.pos.y, self.size, self.size))

        if self.ready_to_reproduce:
            pygame.draw.circle(self.screen, (255, 105, 180), self.pos, self.perception, 1)



class Fruits:
    def __init__(self, protein, x, y, screen):
        self.protein=protein
        self.pos=pygame.math.Vector2(x,y)
        self.size=2
        self.screen=screen
        
        self.color=('white')


    def draw_Fruit(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.size)

