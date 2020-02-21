import need_py_speed_game.Game.variables_for_reaction_time as react_time
import pygame as pg
import os, sys

BLACK = (0, 0, 0)

font_text_title = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_BdIt.ttf', 100)
font_text = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_BdIt.ttf', 50)


def print_space_results(screen):  # if you use space for control the car (variables_for_reaction_time)
    bottom = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'road.png')
    screen.blit(bottom, (0, 0))
    # semi transparent background
    s = pg.Surface((1024, 768))  # size
    s.set_alpha(100)
    s.fill((255, 255, 255))  # this fills the entire surface

    g = pg.Surface((1024, 220))  # green background
    g.set_alpha(100)
    g.fill((0, 255, 0))

    r = pg.Surface((1024, 220))  # red background
    r.set_alpha(100)
    r.fill((255, 0, 0))

    start_text_position_y = 180
    screen.blit(s, (0, 0))  # draw
    screen.blit(g, (0, start_text_position_y - 30))
    screen.blit(r, (0, start_text_position_y + 250))

    green_times, red_times = react_time.count_reaction_time()
    mean_green_time, mean_red_time = react_time.mean_reaction_time(green_times, red_times)
    best_green_time, best_red_time = react_time.best_reaction_time(green_times, red_times)
    score_text_mean_green = font_text.render(
        "Průměrný reakční čas na zelenou: " + str(round(mean_green_time, 2)) + " s", True, BLACK)
    score_text_best_green = font_text.render(
        "Nejlepší reakční čas na zelenou: " + str(round(best_green_time, 2)) + " s", True, BLACK)
    score_text_mean_red = font_text.render("Průměrný reakční čas na červenou: " + str(round(mean_red_time, 2)) + " s",
                                           True, BLACK)
    score_text_best_red = font_text.render("Nejlepší reakční čas na červenou: " + str(round(best_red_time, 2)) + " s",
                                           True, BLACK)
    title_text = "Reakční časy"
    title_text = font_text_title.render(title_text, True, BLACK)
    screen.blit(title_text, [250, 20])

    screen.blit(score_text_mean_green, [20, start_text_position_y])
    screen.blit(score_text_best_green, [20, start_text_position_y + 100])
    screen.blit(score_text_mean_red, [20, start_text_position_y + 280])
    screen.blit(score_text_best_red, [20, start_text_position_y + 380])


def print_emg_results(screen, best, mean):
    font_text_title = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_BdIt.ttf', 100)
    font_text = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_BdIt.ttf', 50)
    bottom = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'road.png')
    screen.blit(bottom, (0, 0))
    # semi transparent background
    s = pg.Surface((1024, 768))  # size
    s.set_alpha(100)
    s.fill((255, 255, 255))  # this fills the entire surface

    g = pg.Surface((1024, 120))
    g.set_alpha(100)
    g.fill((0, 200, 0))

    r = pg.Surface((1024, 120))
    r.set_alpha(100)
    r.fill((200, 0, 0))

    start_text_position_y = 200
    screen.blit(s, (0, 0))  # draw
    screen.blit(g, (0, start_text_position_y - 30))
    screen.blit(r, (0, start_text_position_y + 250))
    score_text_mean = font_text.render(
        "Tvůj průměrný reakční čas: " + str(round(mean, 2)) + " sekund", True, BLACK)
    score_text_best = font_text.render(
        "Tvůj nejlepší reakční čas" + str(round(best, 2)) + " sekund", True, BLACK)
    title_text = "Reakční časy"
    title_text = font_text_title.render(title_text, True, BLACK)
    screen.blit(title_text, [250, 20])

    screen.blit(score_text_mean, [20, start_text_position_y])
    screen.blit(score_text_best, [20, start_text_position_y + 300])
