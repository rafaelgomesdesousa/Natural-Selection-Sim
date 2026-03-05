import pygame
from objects import *
from functions import *


def play_simulation(screen, width, heigth, mode):
    clock=pygame.time.Clock()
    running=True

#Criando Grid
    square_size=50
    background_color=(0,0,0)
    grid_color=(255,255,255)

#Inicializando Arrays dos Objetos
    individuals=[]
    fruits=[]
    shields=[]

#Configurar spawn de fturas por segundos
    time_between_fruits=1000
    last_spawn_fruit=pygame.time.get_ticks()

#Spawna Frutas iniciais
    spawn_Fruits(2000,fruits, width, heigth, screen)

#Spawna Individuos Iniciais

    if mode=="predefined":
        spawn_specific_individuals(25, individuals, width, heigth, 1, 1, screen)     #ENERGY
        spawn_specific_individuals(20, individuals, width, heigth, 2, 2, screen)     #VELOCITY
        spawn_specific_individuals(25, individuals, width, heigth, 3, 3, screen)     #SOCIABILITY
        spawn_specific_individuals(10, individuals, width, heigth, 4, 4, screen)     #ANGRINESS

    elif mode=="create":    
        pass

    type_selected=1

    while running:

    #Event Tracker
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key==pygame.K_1:
                        type_selected=1
                    elif event.key==pygame.K_2:
                        type_selected=2
                    elif event.key==pygame.K_3:
                        type_selected=3
                    elif event.key==pygame.K_4:
                        type_selected=4
                    elif event.key==pygame.K_5:
                        type_selected=5

                    elif event.key==pygame.K_f:
                        type_selected=6

            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                if mode=="create":
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if type_selected==1:
                        new_individual=Individual(5,2,2,2,2, mouse_x, mouse_y, screen)
                    elif type_selected==2:
                        new_individual=Individual(2,5,2,2,2, mouse_x, mouse_y, screen)
                    elif type_selected==3:
                        new_individual=Individual(2,2,5,2,2, mouse_x, mouse_y, screen)
                    elif type_selected==4:
                        new_individual=Individual(2,2,2,5,2, mouse_x, mouse_y, screen)
                    elif type_selected==5:
                        new_individual=Individual(2,2,2,2,5, mouse_x, mouse_y, screen)
                    elif type_selected==6:
                        new_fruit=Fruits(2, mouse_x, mouse_y, screen)
                        fruits.append(new_fruit)

                    individuals.append(new_individual)

#Desenhando Grid
        screen.fill(background_color)
        grid_draw(width, heigth, square_size, grid_color, screen)


#Funcao pra spawnar n frutas por segundo
        current_time=pygame.time.get_ticks()
        if current_time-last_spawn_fruit>time_between_fruits:
            spawn_Fruits(25, fruits, width, heigth, screen) #MUDAR PRA 30 FRUTAS POR SEGUNDO DEPOIS
            #spawn_specific_individuals(10, individuals, width, heigth, 2, 1, screen)   DESCOMENTAR PRA VER OS UPGRADES DOS CARNIVOROS
            
            last_spawn_fruit=current_time

#Funcoes relacionadas aos individuos
#(Draw, Fugir, Reproduzir, Encontrar Parceiro, Caçar, Se mover e Se agrupar)
        for individual in individuals:
            individual.draw_Individual()
            flee(individual, individuals)
            ready_to_reproduce(individual)
            find_mate(individual, individuals)
            hunt(individual, fruits, individuals)

            movement(individual)
            find_group(individual, individuals)

        new_born=[]

#Funcao responsavel por lidar com a criacao de novos individuos
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

#Funcao pra adicionar o escudo nos amarelinhos
        for individual in individuals:
            if "Shield" in individual.skills:
                shields.append(individual)

#Funcao para fazer o escudo dar dano nos predadores
        for shield in shields:
            for individual in individuals:
                if individual.carnivore:
                    if checking_Collision(shield, individual):
                        individual.energy-=0.1

#Desenha frutas
        for fruit in fruits:
            fruit.draw_Fruit()

#Funcao que lida com a alimentacao ("herbivora" e "carnivora")
        for individual in individuals:
            for fruit in fruits[:]:
                #Alimentacao de individuos herbivoros sem skills 
                if checking_Collision(individual, fruit):
                    energy_to_receive=fruit.protein*10

                #Alimentacao de individuos com a skill Leadership
                    if individual.most_significant_gene==3 and "Leadership" not in individual.skills:
                        for leader in individuals:
                            if leader != individual and leader.most_significant_gene==3:
                                if "Leadership" in leader.skills:
                                    if individual.pos.distance_to(leader.pos) <= individual.perception:
                                        tax=energy_to_receive/2

                                        leader.energy+=tax
                                        energy_to_receive-=tax

                                        print(f" IMPOSTO o verdinho beta pagou {tax} pro verdao alfa!")

                                        break

                #Funcao que lida com a alimentacao dos carnivoros e com 
                    if individual.carnivore:
                        #Carnivoros comem as frutas se colidirem com elas, mas recebem 25% da energia apenas
                        individual.energy+=energy_to_receive/4
                    else: 
                        individual.energy+=energy_to_receive

                #Funcao que lida com a alimentacao dos individuos com a skill Socialism
                    if "Socialism" in individual.skills:
                        for friend in individuals:
                            if friend!=individual and friend.most_significant_gene==3:
                                if individual.pos.distance_to(friend.pos)<=individual.perception:
                                    friend.energy+=(energy_to_receive)/2

                    elif individual.most_significant_gene==3:
                        for friend in individuals:
                            if friend!=individual and friend.most_significant_gene==3:
                                if individual.pos.distance_to(friend.pos)<=individual.perception:

                                    friend.energy+=(energy_to_receive)/4

                    fruits.remove(fruit)
            attack(individual, individuals)
        checking_Death(individuals)
        
        clock.tick(60)
        pygame.display.flip()



