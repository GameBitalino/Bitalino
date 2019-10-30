# coding: utf-8

from .track_objects import *
from .fuel import *

pygame.init()
        
lista_musicas = ['Track 01.mp3', 'Track 02.mp3', 'Track 03.mp3', 'Track 04.mp3']
listas_musicas_menu = ['som_menu.mp3', 'som_menu_2.mp3']

song_menu1 = pygame.mixer.Sound('./need_py_speed_game/Game/sons' + os.sep + 'Robot_blip.wav')
song_menu2 = pygame.mixer.Sound('./need_py_speed_game/Game/sons' + os.sep + 'flyby-Conor.wav')

song_come_back = pygame.mixer.Sound('./need_py_speed_game/Game/sons' + os.sep + 'spin_jump.wav')
song_pause = pygame.mixer.Sound('./need_py_speed_game/Game/sons' + os.sep + 'Realistic_Punch.wav')
song_game_over = pygame.mixer.Sound('./need_py_speed_game/Game/sons' + os.sep + 'Game Over.wav')

song_bonus1 = pygame.mixer.Sound('./need_py_speed_game/Game/sons' + os.sep + 'Sleigh Bells Ringing 00_00_00-00_00_00.70.wav')
song_bonus2 = pygame.mixer.Sound('./need_py_speed_game/Game/sons' + os.sep + 'Jolly Laugh.wav')

song_drink = pygame.mixer.Sound('./need_py_speed_game/Game/sons' + os.sep + 'shells_falls.wav')
