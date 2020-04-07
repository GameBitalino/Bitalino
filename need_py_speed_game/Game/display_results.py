import pygame as pg
import os, sys

BLACK = (0, 0, 0)

font_text_title = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_BdIt.ttf', 100)
font_text = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_BdIt.ttf', 50)

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
        "Tvůj nejlepší reakční čas: " + str(round(best, 2)) + " sekund", True, BLACK)
    title_text = "Reakční časy"
    title_text = font_text_title.render(title_text, True, BLACK)
    screen.blit(title_text, [250, 20])

    screen.blit(score_text_mean, [20, start_text_position_y])
    screen.blit(score_text_best, [20, start_text_position_y + 300])
