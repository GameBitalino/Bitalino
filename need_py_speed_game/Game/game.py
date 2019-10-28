# coding: utf-8

import pygame, os, sys, time, pickle
from pygame import *
from .faixa import *
from .carro import *
from .arvores import *
from .bebida import *
from .objetos_pista import *
from .combustivel import *
from .efeitos_sonoros import *
from .menu import *

pygame.init()

# Apresentação do jogo
introducao_jogo()


# Menu Raiz
def game():
    record = 0
    if menu_raiz():  # main menu
        pygame.mixer.music.load('./need_py_speed_game/Game/musicas' + os.sep + 'theme_song' + os.sep + random.choice(lista_musicas))
        tela = pygame.display.set_mode((1024, 768))
        screen = pygame.display.get_surface()
        fundo = pygame.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'road.png')
        pygame.display.set_caption('Need for speed')
        clock = pygame.time.Clock()
        fuel = Combustivel(screen)  # fuel
        car = Carro(screen)  # car
        stripes = [Faixa(screen)]  # stripes
        enemy_car = Carro_inimigo(screen)  # enemy car
        right_trees = [Arvores(screen, 'direita')]  # right trees
        left_trees = [Arvores(screen, 'esquerda')]  # left trees
        pygame.key.set_repeat(1, 1)

        i = 0
        print_fuel = False
        show_fuel = False

        print_drink = False
        show_drink = False
        drink = Bebida(screen)  # drink
        cont_drink = 0

        cont_fuel = 1
        car_speed = 20
        cont_score = 0
        cont_view = 20
        car_crash = False  # car crash

        # Music
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        while True:
            clock.tick(20)
            if i % 200 == 0 and i != 0:
                print_fuel = True
                show_fuel = True

            # Fechar o game/ Pausar o game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif pygame.key.get_pressed()[K_ESCAPE]:
                    pygame.mixer.music.pause()
                    som_pausa.play(0)
                    if menu_sair():
                        game()
                    pygame.mixer.music.unpause()
            ##

            key = pygame.key.get_pressed()  # key
            car.mover_carro(key, car_speed)

            if i % 250 == 0:
                show_drink = True
                print_drink = True

            if i % 10 == 0 and len(right_trees) < 6:
                right_trees.append(Arvores(screen, 'direita'))
                left_trees.append(Arvores(screen, 'esquerda'))
                stripes.append(Faixa(screen))
            tela.blit(fundo, (0, 0))

            for j in range(len(right_trees)):  # right trees
                stripes[j].print_faixa(screen)
                right_trees[j].print_arvore(screen)
                left_trees[j].print_arvore(screen)
                enemy_car.print_objeto(screen)
            if show_fuel:
                fuel.print_comb(screen)
            if show_drink:
                drink.print_bebida(screen)

            car.print_carro(screen)

            # Score
            font = pygame.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'nextwaveboldital.ttf', 55)
            texto_score = font.render("Score", True, PRETO)

            score = cont_score * 10
            texto_valor_score = font.render("%d" % score, True, PRETO)
            screen.blit(texto_score, [370, 15])
            screen.blit(texto_valor_score, [540, 15])
            ##

            # Bonus extra
            if int(score) % 5000 == 0 and score > 0:
                cont_view = 0
                cont_score += 5.0
                bonus = 10
                car_crash = False
                bonus_extra = True

            if cont_view < 20 and bonus_extra:
                font = pygame.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'WeareDepraved.ttf', 80)
                texto_bonus = font.render("YOU ARE FAST", True, VERDE)

                cor_font = VERDE
                score = cont_score * 15
                screen.blit(texto_bonus, [512 - texto_bonus.get_size()[0] / 2, 150])
            else:
                bonus_extra = False
            ##

            # Bonus
            if int(score) % 600 == 0 and score > 0:
                som_bonus1.play(0)
                cont_score += 2.0
                cont_view = 0
                bonus = 2
                cor_font = LARANJA
                car_crash = False

            if int(score) % 1000 == 0 and int(score) % 5000 != 0 and score > 0:
                som_bonus2.play(0)
                cont_score += 5.0
                cont_view = 0
                bonus = 5
                cor_font = VERMELHO
                car_crash = False
            ##

            if cont_view < 20:
                font = pygame.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'nextwaveboldital.ttf', 75)
                texto_good = font.render("+ %d0 BONUS" % bonus, True, cor_font)

                screen.blit(texto_good, [320, 80])
                cont_view += 1

            # Gas
            if cont_fuel < 96:
                font = pygame.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'nextwaveboldital.ttf', 50)
                texto_gasolina = font.render("FUEL", True, PRETO)
                screen.blit(texto_gasolina, [910, 10])

                pygame.draw.rect(screen, PRETO, [950, 55, 20, 100], 3)
                pygame.draw.rect(screen, VERMELHO, [952, 57, 16, 96], 0)
                pygame.draw.rect(screen, BRANCO, [952, 57, 16, cont_fuel], 0)
                cont_fuel += 0.1
            else:
                pygame.mixer.music.stop()
                som_batida.play(0)
                if fim_de_jogo(score):
                    game()
            ##

            pygame.display.update()

            carrorect = car.rect_carro
            objetorect = enemy_car.rect_objeto
            combrect = fuel.rect_comb
            bebidarect = drink.rect_comb

            # Colidir car

            #enemies = newSprite(filename, frames)
            #if pygame.sprite.collide_rect_ratio(0.75)(carrorect, objetorect):
            if carrorect.colliderect(objetorect):
                pygame.mixer.music.stop()
                som_batida.play(0)
                if fim_de_jogo(score):
                    game()

            # Colidir fuel
            if fuel.rect_comb.colliderect(car.rect_carro):
                som_bonus1.play(0)
                Comb = 1000
                show_fuel = False

                cont_fuel -= 1
                cont_view = 0
                car_crash = True

            # Colidir bebida #crash with drink
            if carrorect.colliderect(bebidarect):
                som_bebida.play(0)
                car_speed = 10
                cont_drink = 0
                show_drink = False

            if cont_view < 15 and car_crash:
                cont_score += 1.0
                bonus = 1
                cor_font = AMARELO

            for j in range(len(right_trees)):
                right_trees[j].mover_arvores('direita')
                left_trees[j].mover_arvores('esquerda')
                stripes[j].mover_faixa()
                enemy_car.mover_objeto()
                if print_fuel:
                    print_fuel = fuel.mover_comb(print_fuel)
                if print_drink:
                    print_drink = drink.mover_bebida(print_drink)

            i += 1
            cont_score += 0.1

            # drink effect
            if cont_drink == 75:
                car_speed = 20  # speed car
            cont_drink += 1
            ##


# Iniciar Jogo
