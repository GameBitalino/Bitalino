import need_py_speed_game.Game.variables_for_reaction_time as react_time
import pygame as pg
import os, sys


BLACK = (0, 0, 0)

font_text = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_BdIt.ttf', 50)


def print_results(screen):
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
    screen.blit(s, (0, 0))  # draw
    screen.blit(g, (0, 70))
    screen.blit(r, (0, 370))

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
    screen.blit(score_text_mean_green, [20, 100])
    screen.blit(score_text_best_green, [20, 200])
    screen.blit(score_text_mean_red, [20, 400])
    screen.blit(score_text_best_red, [20, 500])




