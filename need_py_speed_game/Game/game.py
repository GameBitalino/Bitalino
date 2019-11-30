# coding: utf-8


import time as timer
from datetime import datetime
from .stripes import *
from .car import *
from .trees import *
from .star import *
from random import gauss
from .menu import *
from .traffic_lights_static import *
import need_py_speed_game.Game.variables_for_reaction_time as react_time_variables

pygame.init()
game_introduction()


def random_time():
    return int(gauss(8, 2))


# Menu
def game():
    record = 0
    counter_cycles = 0
    if root_menu():  # main menu
        pygame.mixer.music.load(
            './need_py_speed_game/Game/musicas' + os.sep + 'theme_song' + os.sep + random.choice(lista_musicas))
        # screen = pygame.display.set_mode((1024, 768))
        screen = pygame.display.get_surface()
        bottom = pygame.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'road.png')
        pygame.display.set_caption('CAR EMG GAME')
        clock = pygame.time.Clock()
        fuel = Fuel(screen)
        car = Car(screen)
        stripes = [Stripes(screen)]
        enemy_car = EnemyCar(screen)
        # traffic_lights = TrafficLights(screen)
        traffic_lights_static = TrafficLightStatic(screen)
        time_change = random_time() + 3  # after some seconds change the lights (for first time more)
        right_trees = [Trees(screen, 'direita')]  # right trees
        left_trees = [Trees(screen, 'esquerda')]  # left trees
        pygame.key.set_repeat()
        i = 0
        score = 0
        # couter_show_lights_time = 100
        print_fuel = False
        show_fuel = False

        print_star = False
        show_star = False

        stars = Star(screen)
        count_stars = 0

        cont_fuel = 1
        car_speed = 20
        game_speed = car_speed / 200
        cont_score = 0
        cont_view = 20
        car_crash = False  # car crash
        pst_speed = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

        # Music
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        start_time_for_change_lights = timer.time()
        # lights for start game
        # set initialize start_time - reaction time
        react_time_variables.initialize()
        # start bitalino
        menu_leave_game(first=True)

        while True:
            clock.tick(20)
            if i % 200 == 0 and i != 0:
                print_fuel = True
                show_fuel = True

            pom_time = timer.time() - start_time_for_change_lights
            # close or pause game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif pygame.key.get_pressed()[K_SPACE] and traffic_lights_static.color == "red":
                    react_time_variables.react_time_red.append(datetime.now())
                    # pygame.mixer.music.pause()
                    song_pause.play(0)
                    result = menu_leave_game()  # pause game
                    if result:
                        game()  # go to menu
                    elif not result:
                        counter_cycles = 0
                        traffic_lights_static.change_to_green()
                        start_time_for_change_lights = time.time()
                        time_change = random_time()
                        pom_time = timer.time() - start_time_for_change_lights
                    # pygame.mixer.music.unpause()
                elif pom_time > time_change + 3:  # 3 sec for reaction possibility, after game over
                    game_over(score, police=True)
                    if game_over(score, police=True):
                        game()

            key = pygame.key.get_pressed()
            car.move_car(key, car_speed)

            if i % 250 == 0:
                show_star = True
                print_star = True

            if i % 10 == 0 and len(right_trees) < 6:
                right_trees.append(Trees(screen, 'direita'))  # direita = right
                left_trees.append(Trees(screen, 'esquerda'))  # esquerda = left
                stripes.append(Stripes(screen))
            screen.blit(bottom, (0, 0))

            for j in range(len(right_trees)):  # right trees
                stripes[j].print_stripes(screen)
                right_trees[j].print_tree(screen)
                left_trees[j].print_tree(screen)
                enemy_car.print_object(screen)
            if show_fuel:
                fuel.print_fuel(screen)
            if show_star:
                stars.print_star(screen)

            car.print_car(screen)
            # change the color

            if pom_time > time_change and traffic_lights_static.color == "green":
                traffic_lights_static.change_to_red()
            if traffic_lights_static.color == "red":
                counter_cycles += 1
            """
            if traffic_lights_static.color == "red":
                if pygame.key.get_pressed()[K_SPACE]:
                    pygame.mixer.music.pause()
                    song_pause.play(0)
                    if menu_leave_game():
                        game()
                    pygame.mixer.music.unpause()
                elif pom_time > time_change + 3:  # 3 sec for reaction possibility, after game over
                    game_over(score, police=True)
                    if game_over(score, police=True):
                        game()
        """
            traffic_lights_static.print_object()
            if counter_cycles == 1:
                print('added to red set up')
                react_time_variables.set_up_times_red_color.append(datetime.now())
            # Score
            font = pygame.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'nextwaveboldital.ttf', 55)
            texto_score = font.render("Score", True, BLACK)

            score = cont_score * 10
            texto_valor_score = font.render("%d" % score, True, BLACK)
            screen.blit(texto_score, [750, 15])
            screen.blit(texto_valor_score, [920, 15])

            # Bonus extra
            if int(score) % 5000 == 0 and score > 0:
                cont_view = 0
                cont_score += 5.0
                bonus = 10
                car_crash = False
                bonus_extra = True

            if cont_view < 20 and bonus_extra:
                font = pygame.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'WeareDepraved.ttf', 80)
                texto_bonus = font.render("YOU ARE FAST", True, GREEN)

                cor_font = GREEN
                score = cont_score * 15
                screen.blit(texto_bonus, [512 - texto_bonus.get_size()[0] / 2, 350])
            else:
                bonus_extra = False

            # Bonus
            if int(score) % 600 == 0 and score > 0:
                song_bonus1.play(0)
                cont_score += 2.0
                cont_view = 0
                bonus = 2
                cor_font = ORANGE
                car_crash = False

            if int(score) % 1000 == 0 and int(score) % 5000 != 0 and score > 0:
                song_bonus2.play(0)
                cont_score += 5.0
                cont_view = 0
                bonus = 5
                cor_font = RED
                car_crash = False

            if cont_view < 20:
                font = pygame.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'nextwaveboldital.ttf', 75)
                texto_good = font.render("+ %d0 BONUS" % bonus, True, cor_font)

                screen.blit(texto_good, [320, 280])
                cont_view += 1

            if cont_fuel < 96:
                font = pygame.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'nextwaveboldital.ttf', 50)
                texto_gasolina = font.render("FUEL", True, BLACK)
                screen.blit(texto_gasolina, [10, 10])
                pygame.draw.rect(screen, BLACK, [50, 55, 20, 100], 3)
                pygame.draw.rect(screen, RED, [52, 57, 16, 96], 0)
                pygame.draw.rect(screen, WHITE, [52, 57, 16, cont_fuel], 0)
                cont_fuel += 0.1
            else:
                pygame.mixer.music.stop()
                song_game_over.play(0)
                if game_over(score):
                    game()

            pygame.display.update()

            car_rect = car.rect_car.inflate(-50, -50)
            enemy_car_rect = enemy_car.rect_objeto.inflate(-30, -30)
            #  pygame.draw.rect(screen, (50, 55, 55), enemy_car_rect)
            fuel_rect = fuel.rect_fuel.inflate(-20, -20)
            star_rect = stars.rect_comb.inflate(-10, -10)

            # Collision with car
            if car_rect.colliderect(enemy_car_rect):
                pygame.mixer.music.stop()
                song_game_over.play(0)
                if game_over(score):
                    game()

            # Collision with fuel
            if fuel_rect.colliderect(car.rect_car):
                song_bonus1.play(0)
                Comb = 1000
                show_fuel = False

                cont_fuel -= 1
                cont_view = 0
                car_crash = True

            # crash with star
            if car_rect.colliderect(star_rect):
                song_drink.play(0)
                car_speed += random.choice(pst_speed)
                count_stars += 0.15
                show_star = False

            if cont_view < 15 and car_crash:
                cont_score += 1
                bonus = 1
                cor_font = YELLOW

            for j in range(len(right_trees)):
                game_speed = car_speed / 200
                right_trees[j].move_tree('direita', game_speed)
                left_trees[j].move_tree('esquerda', game_speed)
                stripes[j].move_stripes(car_speed / 25)
                enemy_car.move_object(game_speed)
                if print_fuel:
                    print_fuel = fuel.move_fuel(print_fuel, game_speed)
                if print_star:
                    print_star = stars.move_star(print_star, game_speed)

            i += 1
            cont_score += 0.1
            """
            print('set_up_green: ', react_time_variables.set_up_times_green_color)
            print('set_up_red: ', react_time_variables.set_up_times_red_color)
            print('react_time_green: ', react_time_variables.react_time_green)
            print('react_time_red: ', react_time_variables.react_time_red)
            """