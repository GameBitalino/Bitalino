# coding: utf-8
from datetime import datetime
import pickle
from pygame import *

from need_py_speed_game.Game.game import start_measure_calm_emg
from .sounds_effects import *
from .traffic_lights_static import *
import need_py_speed_game.Game.variables_for_reaction_time as reaction_time_variables
from .display_results import *
from .checkbox import checkbox
import need_py_speed_game.Game.method as chosen_method

pg.init()


def game_introduction():
    import time
    def position_image_start(imagem, tam_tela):
        largura_imagem, altura_imagem = imagem.get_size()
        largura, altura = tam_tela
        return [(largura / 2) - (largura_imagem / 2), (altura / 2) - (altura_imagem / 2)]

    # load sons
    pg.mixer.pre_init(44100, -16, 2, 2048)
    pg.mixer.music.load('./need_py_speed_game/Game/musicas' + os.sep + 'Tema_PS2.mp3')
    pg.mixer.music.play(1)

    # Load image
    vut = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'vut.png').convert()

    # Load Fonts
    fonte = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_Bd.TTF', 100)
    texto_apresentacao = fonte.render("EMG car game", True, WHITE)
    screen.fill(WHITE)
    screen.blit(vut, position_image_start(vut, size))
    pg.display.update()
    time.sleep(2)

    screen.fill(BLACK)
    screen.blit(texto_apresentacao, position_image_start(texto_apresentacao, size))
    pg.display.update()
    time.sleep(2)
    chosen_method.initialize_method()  # initialize method


def source_position(imagem, pos_inicial):
    x, y = pg.mouse.get_pos()
    largura, altura = imagem.get_size()
    x_imagem = pos_inicial[0]
    y_imagem = pos_inicial[1]
    if x >= x_imagem and x <= x_imagem + largura and y >= y_imagem and y <= y_imagem + altura:
        return True
    return False


def menu_reset():
    while True:
        menu = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'fundo_menu2.jpg').convert()
        screen.blit(menu, [0, 0])
        # pg.draw.rect(screen, WHITE, [100, 600, 10, 50], 0)

        fonte_menu1 = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_BdIt.ttf', 45)
        fonte_menu2 = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_BdIt.ttf', 55)

        texto1 = fonte_menu1.render('Veškeré záznamy budou smazány.', True, WHITE)
        texto2 = fonte_menu1.render('Opravdu chcete pokračovat?', True, WHITE)
        texto3 = fonte_menu2.render('ANO', True, WHITE)
        texto4 = fonte_menu2.render('NE', True, WHITE)

        screen.blit(texto1, [(largura_tela / 2) - (texto1.get_size()[0] / 2), 250])
        screen.blit(texto2, [(largura_tela / 2) - (texto2.get_size()[0] / 2), 300])
        screen.blit(texto3, [400, 384])
        screen.blit(texto4, [550, 384])

        if source_position(texto3, [400, 384]):
            screen.blit(fonte_menu2.render('ANO', True, RED), [400, 384])
        elif source_position(texto4, [550, 384]) or pg.key.get_pressed()[K_ESCAPE]:
            screen.blit(fonte_menu2.render('NE', True, RED), [550, 384])

        for event in pg.event.get():
            if (pg.mouse.get_pressed()[0] and source_position(texto3, [400, 384])):
                with open('./need_py_speed_game/Game/salve_recordes' + os.sep + 'save_record.dat', 'wb') as f:
                    pickle.dump(0, f, 2)
                return True
            elif (pg.mouse.get_pressed()[0] and source_position(texto4, [550, 384])) or pg.key.get_pressed()[
                K_ESCAPE]:
                song_come_back.play(0)
                return True
            elif event.type == pg.QUIT:
                sys.exit()

        pg.display.update()


def menu_settings():
    menu = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'fundo_menu2.jpg')
    fonte_menu1 = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_BdIt.ttf', 70)
    fonte_menu2 = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_BdIt.ttf', 50)

    texto1 = fonte_menu1.render('METODA DETEKCE EMG', True, WHITE)
    option1 = fonte_menu2.render('Nelineární metoda TKEO', True, WHITE)
    option2 = fonte_menu2.render('Klasifikátor SVM', True, WHITE)
    option3 = fonte_menu2.render('Neuronová síť UNet', True, WHITE)
    tkeoCheckbox = checkbox(screen, 40, 205)
    svmCheckoubox = checkbox(screen, 40, 305)
    unetCheckbox = checkbox(screen, 40, 405)
    if chosen_method.choose_method == "UNET":
        unetCheckbox.checked = True
    elif chosen_method.choose_method == "SVM":
        svmCheckoubox.checked = True
    elif chosen_method.choose_method == "TKEO":
        tkeoCheckbox.checked = True

    texto3 = fonte_menu1.render('Zpět', True, WHITE)

    while True:
        screen.blit(menu, [0, 0])
        screen.blit(texto1, [(largura_tela / 2) - (texto1.get_size()[0] / 2), 40])
        screen.blit(option1, [140, 200])
        tkeoCheckbox.render_checkbox()
        svmCheckoubox.render_checkbox()
        unetCheckbox.render_checkbox()
        screen.blit(option2, [140, 300])
        screen.blit(option3, [140, 400])
        screen.blit(texto3, [750, 650])

        if source_position(texto3, [750, 650]) or pg.key.get_pressed()[K_ESCAPE]:
            screen.blit(fonte_menu1.render('Zpět', True, RED), [750, 650])

        for event in pg.event.get():
            if tkeoCheckbox.update_checkbox(event) and tkeoCheckbox.is_checked():
                svmCheckoubox.checked = False
                svmCheckoubox.render_checkbox()
                unetCheckbox.checked = False
                unetCheckbox.render_checkbox()
                chosen_method.change_method_to("TKEO")
            elif svmCheckoubox.update_checkbox(event) and svmCheckoubox.is_checked():
                unetCheckbox.checked = False
                unetCheckbox.render_checkbox()
                tkeoCheckbox.checked = False
                tkeoCheckbox.render_checkbox()
                chosen_method.change_method_to("SVM")
            elif unetCheckbox.update_checkbox(event) and unetCheckbox.is_checked():
                svmCheckoubox.checked = False
                svmCheckoubox.render_checkbox()
                tkeoCheckbox.checked = False
                tkeoCheckbox.render_checkbox()
                chosen_method.change_method_to("UNET")

            if (pg.mouse.get_pressed()[0] and source_position(texto3, [750, 650])) or pg.key.get_pressed()[
                K_ESCAPE]:
                song_come_back.play(0)
                return True
            elif event.type == pg.QUIT:
                sys.exit()
        pg.display.update()


def menu_record():
    # load Record
    with open('./need_py_speed_game/Game/salve_recordes' + os.sep + 'save_record.dat', 'rb') as f:
        record = pickle.load(f)

    menu = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'menu_recorde.jpg')
    fonte_menu1 = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_BdIt.ttf', 70)
    fonte_menu2 = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_BdIt.ttf', 50)

    texto1 = fonte_menu1.render('REKORD', True, WHITE)
    texto2 = fonte_menu2.render('Nejlepší skóre  =  %d' % record, True, WHITE)
    texto3 = fonte_menu1.render('Zpět', True, WHITE)

    while True:
        screen.blit(menu, [0, 0])
        screen.blit(texto1, [(largura_tela / 2) - (texto1.get_size()[0] / 2), 20])
        screen.blit(texto2, [20, 200])
        screen.blit(texto3, [750, 650])

        if source_position(texto3, [750, 650]) or pg.key.get_pressed()[K_ESCAPE]:
            screen.blit(fonte_menu1.render('Zpět', True, RED), [750, 650])

        for event in pg.event.get():
            if (pg.mouse.get_pressed()[0] and source_position(texto3, [750, 650])) or pg.key.get_pressed()[
                K_ESCAPE]:
                song_come_back.play(0)
                return True
            elif event.type == pg.QUIT:
                sys.exit()

        pg.display.update()


# Menu help
def menu_help():
    menu = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'fundo_menu2.jpg')
    tecla1 = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'computer_key_Arrow_Left.png')
    tecla2 = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'computer_key_Arrow_Right.png')
    tecla3 = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'computer_key_Esc.png')
    fonte_menu3 = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_Lt.ttf', 55)
    fonte_menu4 = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_Lt.ttf', 40)

    texto1 = fonte_menu3.render('Nápověda', True, WHITE)

    texto2 = fonte_menu4.render('Ovládání hry', True, WHITE)
    texto3 = fonte_menu4.render('Vyhýbejte se protijedoucím vozidlům,', True, WHITE)
    texto4 = fonte_menu4.render('Zastavte co nejrychleji na červenou', True, WHITE)
    texto5 = fonte_menu4.render('Na zelenou se co nejrychleji rozjeďte.', True, WHITE)
    texto6 = fonte_menu4.render('Nikdy nesmí dojít palivo - doplníte sebráním benzínu', True, WHITE)

    texto7 = fonte_menu4.render('Jaké klávesy použít?', True, WHITE)
    texto8 = fonte_menu4.render('Řízení auta: vlevo/vpravo', True, WHITE)
    texto9 = fonte_menu4.render('Pauza / Hra', True, WHITE)

    texto10 = fonte_menu3.render('Zpět', True, WHITE)
    while True:
        screen.blit(menu, [0, 0])
        screen.blit(pg.transform.scale(tecla1, [50, 50]), [20, 480])
        screen.blit(pg.transform.scale(tecla2, [50, 50]), [80, 480])
        screen.blit(pg.transform.scale(tecla3, [50, 50]), [20, 550])
        screen.blit(texto1, [(largura_tela / 2) - (texto1.get_size()[0] / 2), 10])
        screen.blit(texto2, [20, 100])
        screen.blit(texto3, [40, 170])
        screen.blit(texto4, [40, 220])
        screen.blit(texto5, [40, 270])
        screen.blit(texto6, [40, 320])

        screen.blit(texto7, [20, 390])
        screen.blit(texto8, [150, 480])
        screen.blit(texto9, [150, 550])

        screen.blit(texto10, [800, 650])

        if source_position(texto10, [800, 650]) or pg.key.get_pressed()[K_ESCAPE]:
            screen.blit(fonte_menu3.render('Zpět', True, RED), [800, 650])

        for event in pg.event.get():
            if (pg.mouse.get_pressed()[0] and source_position(texto9, [800, 650])) or pg.key.get_pressed()[
                K_ESCAPE]:
                song_come_back.play(0)
                return True
            elif event.type == pg.QUIT:
                sys.exit()

        pg.display.update()


# after pause game
def menu_leave_game(red_for_sec=5, first=False):
    if first:
        bottom = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'road.png')
        screen.blit(bottom, (0, 0))
    escape = 0
    traffic_lights = TrafficLightStatic(screen, "red")
    start_time = time.time()
    font_text = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_BdIt.ttf', 100)
    # semi transparent
    s = pygame.Surface((1024, 150))  # size
    s.set_alpha(150)
    s.fill((255, 255, 255))  # this fills the entire surface
    screen.blit(s, (0, 380))  # draw
    text_waiting = font_text.render("Počkej na zelenou", True, BLACK)

    while True:
        counter_cycles = 0
        if time.time() - start_time > red_for_sec and traffic_lights.color == "red":
            traffic_lights.change_to_green()
            counter_cycles += 1
            s = pygame.Surface((1024, 150))  # size
            s.set_alpha(250)
            s.fill((255, 255, 255))  # this fills the entire surface
            screen.blit(s, (0, 380))  # draw
            text_waiting = font_text.render("Pokračuj v jízdě", True, BLACK)
        screen.blit(text_waiting, [(512 - text_waiting.get_size()[0] / 2), 400])
        traffic_lights.print_object()
        if counter_cycles == 1:
            reaction_time_variables.set_up_times_green_color.append(datetime.now())
        # add to vector of time when changed_to_green

        for event in pg.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif pygame.key.get_pressed()[K_SPACE] and traffic_lights.color == "green":
                print('after press SPACE on green')
                reaction_time_variables.react_time_green.append(datetime.now())  # change after add signal
                return False
            elif pygame.key.get_pressed()[K_ESCAPE]:
                song_come_back.play(0)
                return True
            elif escape > 1000000:
                return True

        pg.display.update()
        escape += 1


def OK_button_results(screen):
    text = 'OK'
    button_text = font_text.render(text, True, BLACK)
    position = [870, 680]
    screen.blit(button_text, position)
    if source_position(button_text, position):
        screen.blit(font_text.render(text, True, RED), position)
    for event in pg.event.get():
        if (pg.mouse.get_pressed()[0] and source_position(button_text, position)) or pg.key.get_pressed()[pg.K_ESCAPE]:
            return True
        elif event.type == pg.QUIT:
            sys.exit()


# Game Over
def game_over(score, police=False):
    green_score, red_score = reaction_time_variables.count_reaction_time()
    print('reaction time on red traffic lights: ', red_score)
    print('reaction time on green traffic lights: ', green_score)
    score = int(score)
    print_record = False

    policeMan = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'police.png')
    # load records
    with open('./need_py_speed_game/Game/salve_recordes' + os.sep + 'save_record.dat', 'rb') as f:
        record = pickle.load(f)

    if score > record:
        record = score
        # save record
        with open('./need_py_speed_game/Game/salve_recordes' + os.sep + 'save_record.dat', 'wb') as f:
            pickle.dump(score, f, 2)
            print_record = True

            fonte_record = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'nextwaveboldital.ttf', 90)
            texto_record = fonte_record.render("NEW RECORD", True, ORANGE_2)
            texto_score = fonte_record.render("%d" % record, True, ORANGE_2)

    while True:
        fonte_fim = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'JUSTFIST2.ttf', 70)
        texto_fim = fonte_fim.render("GAME OVER", True, RED)
        s = pygame.Surface((1024, 150))  # size
        s.set_alpha(150)
        s.fill((255, 255, 255))  # this fills the entire surface
        screen.blit(s, (0, 380))  # draw
        screen.blit(texto_fim, [(1024 / 2) - (texto_fim.get_size()[0] / 2), 420])
        if police:
            screen.blit(policeMan, (700, 250))

        if print_record:
            screen.blit(texto_record, [(1024 / 2) - (texto_record.get_size()[0] / 2), 100])
            screen.blit(texto_score, [(1024 / 2) - (texto_score.get_size()[0] / 2), 150])

        pg.display.update()
        pg.time.delay(3000)
        # reaction time results - display it
        print_results(screen)
        results = False
        while not results:
            results = OK_button_results(screen)
            pg.display.update()
        pg.time.delay(1000)
        return True


# Menu Principal
def root_menu():
    # Load fonts
    fonte_menu = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_BdIt.ttf', 60)
    font_menu_items = pg.font.Font('./need_py_speed_game/Game/fontes' + os.sep + 'Aller_BdIt.ttf', 55)

    text_menu = fonte_menu.render("RACING GAME", True, YELLOW)

    play_text = font_menu_items.render("Hrát", True, YELLOW)
    help_text = font_menu_items.render("Nápověda", True, YELLOW)
    record_text = font_menu_items.render("Rekord", True, YELLOW)
    settings_text = font_menu_items.render("Nastavení", True, YELLOW)
    remove_record_text = font_menu_items.render("Smazat záznamy", True, YELLOW)
    exit_text = font_menu_items.render("Konec", True, YELLOW)

    # Som do menu
    pg.mixer.pre_init(44100, -16, 2, 2048)
    pg.mixer.music.load('./need_py_speed_game/Game/musicas' + os.sep + random.choice(listas_musicas_menu))
    pg.mixer.music.play(-1)
    pg.mixer.music.set_volume(1)

    menu = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'fundo_menu.jpg')
    while True:
        # Imagem do menu
        screen.blit(menu, [0, 0])
        screen.blit(text_menu, [(largura_tela / 2) - (text_menu.get_size()[0] / 2), 30])
        screen.blit(play_text, [40, 150])
        screen.blit(help_text, [40, 250])
        screen.blit(record_text, [40, 350])
        screen.blit(settings_text, [40, 450])
        screen.blit(remove_record_text, [40, 550])
        screen.blit(exit_text, [40, 650])

        if source_position(play_text, [40, 150]):
            screen.blit(font_menu_items.render("Hrát", True, RED), [40, 150])
        elif source_position(help_text, [40, 250]):
            screen.blit(font_menu_items.render("Nápověda", True, RED), [40, 250])
        elif source_position(record_text, [40, 350]):
            screen.blit(font_menu_items.render("Rekord", True, RED), [40, 350])
        elif source_position(settings_text, [40, 450]):
            screen.blit(font_menu_items.render("Nastavení", True, RED), [40, 450])
        elif source_position(remove_record_text, [40, 550]):
            screen.blit(font_menu_items.render("Smazat záznamy", True, RED), [40, 550])
        elif source_position(exit_text, [40, 650]):
            screen.blit(font_menu_items.render("Konec", True, RED), [40, 650])

        for event in pg.event.get():
            if pg.mouse.get_pressed()[0] and source_position(play_text, [40, 150]):
                song_menu2.play(0)
                pg.mixer.music.stop()
                # start game
                start_measure_calm_emg()
                return True
            elif pg.mouse.get_pressed()[0] and source_position(help_text, [40, 250]):
                song_menu1.play(0)
                if menu_help():
                    continue
            elif pg.mouse.get_pressed()[0] and source_position(record_text, [40, 350]):
                song_menu1.play(0)
                if menu_record():
                    continue
            elif pg.mouse.get_pressed()[0] and source_position(remove_record_text, [40, 450]):
                song_menu1.play(0)
                if menu_settings():
                    continue
            elif pg.mouse.get_pressed()[0] and source_position(remove_record_text, [40, 550]):
                song_menu1.play(0)
                if menu_reset():
                    continue
            elif pg.mouse.get_pressed()[0] and source_position(exit_text, [40, 650]):
                sys.exit()
            elif event.type == pg.QUIT:
                sys.exit()

        pg.display.update()


# Configuration screen
size = largura_tela, altura_leta = (1024, 768)
screen = pg.display.set_mode(size)
pg.display.set_caption('EMG game')

# Load cores
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
ORANGE_2 = (251, 79, 12)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (51, 181, 205)
BLUE_2 = (0, 0, 255)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
GRAY2 = (190, 190, 190)
