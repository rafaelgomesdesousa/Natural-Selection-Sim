import pygame
from objects import *
from functions import *
from database import *


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

#Iniciando coisas pro banco de dados

    species_peak = {0:0, 1:0, 2:0, 3:0, 4:0}
    maximum_generation = {0:1, 1:1, 2:1, 3:1, 4:1}
    
    initial_population = {0:0, 1:0, 2:0, 3:0, 4:0}
    final_population = {0:0, 1:0, 2:0, 3:0, 4:0}
    alive_individuals_now = {0:0, 1:0, 2:0, 3:0, 4:0}

    initial_perceptors=25
    initial_energizeds=25
    initial_velociters=20
    initial_socialists=25
    initial_ragers=10

    total_seconds=0

    total_born=0
    total_deaths=0

#Spawna Individuos Iniciais

    if mode=="predefined":
        spawn_specific_individuals(initial_perceptors, individuals, width, heigth, 1, 1, screen)     #PERCEPTION
        spawn_specific_individuals(initial_energizeds, individuals, width, heigth, 1, 1, screen)     #ENERGY
        spawn_specific_individuals(initial_velociters, individuals, width, heigth, 2, 2, screen)     #VELOCITY
        spawn_specific_individuals(initial_socialists, individuals, width, heigth, 3, 3, screen)     #SOCIABILITY
        spawn_specific_individuals(initial_ragers, individuals, width, heigth, 4, 4, screen)     #ANGRINESS

    elif mode=="create":    
        pass

    type_selected=1

    for individual in individuals:
        gene = individual.most_significant_gene
        if gene in initial_population:
            initial_population[gene] += 1

    while running:

    #Event Tracker
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:

                        simulation_id=save_simulation_log(mode, total_seconds, total_born, total_deaths)

                        final_population = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
                        for individual in individuals:
                            gene = individual.most_significant_gene
                            if gene in final_population:
                                final_population[gene] += 1

                        data_to_insert=[]

                        for gene in range(5):
                            line=(
                                simulation_id,
                                gene,
                                initial_population[gene],
                                final_population[gene],
                                species_peak[gene],
                                maximum_generation[gene]
                            )
                            data_to_insert.append(line)

                        save_species_performance(data_to_insert)

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
    #Tudo que estiver dentro desse if sera executado a cada 1 segundo
        if current_time-last_spawn_fruit>time_between_fruits:
            spawn_Fruits(25, fruits, width, heigth, screen) #MUDAR PRA 30 FRUTAS POR SEGUNDO DEPOIS
            #spawn_specific_individuals(10, individuals, width, heigth, 2, 1, screen)   DESCOMENTAR PRA VER OS UPGRADES DOS CARNIVOROS
            total_seconds+=1
            alive_individuals_now={0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

            for individual in individuals:
                gene=individual.most_significant_gene
                if gene in alive_individuals_now:
                    alive_individuals_now[gene]+=1

            for gene in species_peak:
                if alive_individuals_now[gene]>species_peak[gene]:
                    species_peak[gene]=alive_individuals_now[gene]
            
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

                    child=Individual(new_genes[0],
                                    new_genes[1],
                                    new_genes[2],
                                    new_genes[3],
                                    new_genes[4],
                                    individual.pos.x,
                                    individual.pos.y,
                                    individual.screen)
                    
                    total_born+=1
                    child.generation=max(individual.generation, individual.mate_target.generation)+1
                    individual.mate_target=None
                    
                    new_born.append(child)

                    gene_child=child.most_significant_gene
                    if child.generation>maximum_generation[gene_child]:
                        maximum_generation[gene_child]=child.generation


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
        deaths_now=checking_Death(individuals)
        total_deaths+=deaths_now
        
        clock.tick(60)
        pygame.display.flip()



