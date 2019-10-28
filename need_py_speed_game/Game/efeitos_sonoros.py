# coding: utf-8

from .objetos_pista import *
from .combustivel import *

pygame.init()
        
lista_musicas = ['Track 01.mp3', 'Track 02.mp3', 'Track 03.mp3', 'Track 04.mp3']
listas_musicas_menu = ['som_menu.mp3', 'som_menu_2.mp3']

som_menu1 = pygame.mixer.Sound('./need_py_speed_game/Game/sons' + os.sep + 'Robot_blip.wav')
som_menu2 = pygame.mixer.Sound('./need_py_speed_game/Game/sons' + os.sep + 'flyby-Conor.wav')

som_voltar = pygame.mixer.Sound('./need_py_speed_game/Game/sons' + os.sep + 'spin_jump.wav')
som_pausa = pygame.mixer.Sound('./need_py_speed_game/Game/sons' + os.sep + 'Realistic_Punch.wav')
som_batida = pygame.mixer.Sound('./need_py_speed_game/Game/sons' + os.sep + 'Game Over.wav')

som_bonus1 = pygame.mixer.Sound('./need_py_speed_game/Game/sons' + os.sep + 'Sleigh Bells Ringing 00_00_00-00_00_00.70.wav')
som_bonus2 = pygame.mixer.Sound('./need_py_speed_game/Game/sons' + os.sep + 'Jolly Laugh.wav')

som_bebida = pygame.mixer.Sound('./need_py_speed_game/Game/sons' + os.sep + 'shells_falls.wav')
