# coding: utf-8
import time as timer
from .stripes import *
from .car import *
from .trees import *
from .star import *
from random import gauss
from .menu import *
from .traffic_lights_static import *
from measured_data_bitalino_global import OnlineProcessing, reaction_times_init, reaction_times_add_time
import need_py_speed_game.Game.method as chosen_method
from datetime import datetime

pygame.init()
game_introduction()


def random_time():
    return int(gauss(8, 2))


def start_measure_calm_emg():
    global background
    pygame.event.pump()
    background = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'road.png')
    font_text = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_BdIt.ttf', 85)
    # semi transparent
    s = pygame.Surface((1024, 150))  # size
    s.set_alpha(150)
    s.fill((255, 255, 255))  # this fills the entire surface
    text_waiting = font_text.render("Měření klidového signálu", True, BLACK)
    # visible for user
    screen.blit(background, (0, 0))
    screen.blit(s, (0, 380))  # draw
    screen.blit(text_waiting, [(512 - text_waiting.get_size()[0] / 2), 400])
    pg.display.update()

    global device, result
    # connect and start bitalino, initialize method
    device = OnlineProcessing(chosen_method.chosen_method())
    result = False
    start_time = time.time()
    while (time.time() - start_time) < 3 and not result:
        # pygame.event.get()
        pygame.event.pump()
        screen.blit(background, (0, 0))
        screen.blit(s, (0, 380))  # draw
        screen.blit(text_waiting, [(512 - text_waiting.get_size()[0] / 2), 400])
        result = device.process_data()
        pg.display.update()
    if chosen_method.chosen_method() == "UNET":
        pass
    else:
        text_waiting = font_text.render("Zatni sval maximální silou", True, BLACK)
        start_time = time.time()
        while (time.time() - start_time) <1:
            # pygame.event.get()
            pygame.event.pump()
            screen.blit(background, (0, 0))
            screen.blit(s, (0, 380))  # draw
            screen.blit(text_waiting, [(512 - text_waiting.get_size()[0] / 2), 400])
            result = device.process_data()
            if result:
                device.count_max_of_signal()  # edit maximum of signal
                return False
            pg.display.update()


def end_measure_emg():
    global device, reaction_time
    device.save_EMG()
    reaction_time = device.count_reaction_time()
    return reaction_time


def change_lights(traffic_lights_static, from_pause=False):
    global device, pom_time, score, time_change
    result_emg = device.process_data()
    if not from_pause:
        if result_emg and traffic_lights_static.color == "red":
            song_pause.play(0)
            result = menu_leave_game()  # pause game
            if result:
                game()  # go to menu
            else:
                traffic_lights_static.change_to_green()
                start_time_for_change_lights = time.time()
                time_change = random_time()
                pom_time = timer.time() - start_time_for_change_lights
        elif pom_time > time_change + 3:  # 3 sec for reaction possibility, after game over
            game_over(score, police=True)
            if game_over(score, police=True):
                game()
    else:
        if result_emg and traffic_lights_static.color == "green":
            print('after EMG activity on green lights')
            return False
        else:
            return True


# Menu
def game():
    record = 0
    counter_cycles = 0
    global pom_time, time_change, score, background, device, display_car, traffic_lights_static
    pygame.mixer.music.load(
        './need_py_speed_game/Game/musicas' + os.sep + 'theme_song' + os.sep + random.choice(lista_musicas))
    if root_menu():  # main menu
        # screen = pygame.display.set_mode((1024, 768))
        screen = pygame.display.get_surface()
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
        car_speed = 40
        game_speed = car_speed / 200
        cont_score = 0
        cont_view = 20
        car_crash = False  # car crash
        pst_speed = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

        # Music
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1)

        # fonts
        font_score = pygame.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'nextwaveboldital.ttf', 55)
        texto_score = font_score.render("Score", True, BLACK)
        font_bonus = pygame.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'WeareDepraved.ttf', 80)
        texto_bonus = font_bonus.render("YOU ARE FAST", True, GREEN)
        cor_font = GREEN
        font_fuel = pygame.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'nextwaveboldital.ttf', 50)
        texto_gasolina = font_fuel.render("FUEL", True, BLACK)
        font_bonus = pygame.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'nextwaveboldital.ttf', 75)

        # start bitalino
        # calm EMG
        reaction_times_init()  # initialize variables for reaction time
        menu_leave_game(first=True)
        start_time_for_change_lights = timer.time()

        while True:
            clock.tick(20)
            pygame.event.get()
            if i % 200 == 0 and i != 0:
                print_fuel = True
                show_fuel = True
            pom_time = timer.time() - start_time_for_change_lights
            # change_lights(traffic_lights_static, from_pause=False, ambulance_valuing=enemy_car.is_ambulance)
            # according to EMG
            # global device
            result_emg = device.process_data()
            if result_emg and enemy_car.is_ambulance:
                enemy_car.ambulance_music.stop()
                display_car = False
            elif enemy_car.is_ambulance and traffic_lights_static.color == "red":
                display_car = False
                enemy_car.is_ambulance = False
                enemy_car.witch_object = 2
            elif not enemy_car.is_ambulance:
                display_car = True
            if result_emg and traffic_lights_static.color == "red":
                song_pause.play(0)
                result = menu_leave_game()  # pause game
                if result:
                    game()  # go to menu
                else:
                    counter_cycles = 0
                    traffic_lights_static.change_to_green()
                    start_time_for_change_lights = time.time()
                    time_change = random_time()
                    pom_time = timer.time() - start_time_for_change_lights
            elif traffic_lights_static.color == "red" and timer.time() > time_change + 3:  # 3 sec for reaction possibility, after game over
                print(pom_time)
                print(time_change)
                game_over(score, police=True)
                if game_over(score, police=True):
                    game()

            if enemy_car.first:
                display_car = True
            # right left movement
            for event in pygame.event.get():
                print(event)
            key = pygame.key.get_pressed()
            car.move_car(key, car_speed)

            if i % 250 == 0:
                show_star = True
                print_star = True

            if i % 10 == 0 and len(right_trees) < 6:
                right_trees.append(Trees(screen, 'direita'))  # direita = right
                left_trees.append(Trees(screen, 'esquerda'))  # esquerda = left
                stripes.append(Stripes(screen))
            screen.blit(background, (0, 0))

            for j in range(len(right_trees)):  # right trees
                stripes[j].print_stripes(screen)
                right_trees[j].print_tree(screen)
                left_trees[j].print_tree(screen)

            enemy_car.print_object(print_car=display_car)

            if show_fuel:
                fuel.print_fuel(screen)
            if show_star:
                stars.print_star(screen)

            car.print_car(screen)
            # change the color
            if pom_time > time_change and traffic_lights_static.color == "green" and not enemy_car.is_ambulance:
                traffic_lights_static.change_to_red()
                time_change = timer.time()
            if traffic_lights_static.color == "red":
                counter_cycles += 1
            traffic_lights_static.print_object()

            # Score
            score = cont_score * 10
            texto_valor_score = font_score.render("%d" % score, True, BLACK)
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
                score = cont_score * 15
                screen.blit(font_bonus, [512 - texto_bonus.get_size()[0] / 2, 350])
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
                texto_good = font_bonus.render("+ %d0 BONUS" % bonus, True, cor_font)
                screen.blit(texto_good, [320, 280])
                cont_view += 1

            if cont_fuel < 96:
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
            if counter_cycles == 1:  # change to red
                reaction_times_add_time(datetime.now())
            if enemy_car.is_ambulance and enemy_car.first:
                enemy_car.ambulance_music.play()
                reaction_times_add_time(datetime.now(), ambulance=True)
            elif not enemy_car.is_ambulance or not display_car:
                enemy_car.ambulance_music.stop()

            car_rect = car.rect_car.inflate(-50, -50)
            enemy_car_rect = enemy_car.rect_objeto.inflate(-30, -30)
            #  pygame.draw.rect(screen, (50, 55, 55), enemy_car_rect)
            fuel_rect = fuel.rect_fuel.inflate(-20, -20)
            star_rect = stars.rect_comb.inflate(-10, -10)

            # Collision with car
            if car_rect.colliderect(enemy_car_rect) and display_car:  # no crash after disappear ambulance
                pygame.mixer.music.stop()
                song_game_over.play(0)
                if game_over(score):
                    game()

            if enemy_car.game_over:
                print("No reaction on ambulance car...")
                game_over(score, police=True)

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
