# coding: utf-8

import pygame, os, sys, time, random, pickle
from pygame import *
from efeitos_sonoros import *
pygame.init()

# Intrudução do jogo
def introducao_jogo():
    import time
    def posicao_imagem_inicio(imagem, tam_tela):
      largura_imagem , altura_imagem = imagem.get_size()
      largura, altura = tam_tela
      
      return [(largura / 2) - (largura_imagem / 2),(altura / 2) - (altura_imagem / 2)]
    
    # Carregando sons
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.music.load('musicas' + os.sep + 'Tema_PS2.mp3')
    pygame.mixer.music.play(1)
    
    # Carregando imagens
    ufcg = pygame.image.load('imagens' + os.sep + 'logo_ufcg.png').convert()
    cc = pygame.image.load('imagens' + os.sep + 'logo_computacao.jpg').convert()
    logo_jogo = pygame.image.load('imagens' + os.sep + 'logo_jogo.jpg').convert()
    
    # Carregando Fonte Inicio
    fonte = pygame.font.Font('fontes' + os.sep + 'btseps2.TTF',200)
    texto_apresentacao = fonte.render("Car game",True,CINZA)
    # Sequencias de imagens
    tela.fill(BRANCO)
    tela.blit(ufcg, posicao_imagem_inicio(ufcg, tam_tela))
    pygame.display.update()
    time.sleep(5)
    
    tela.fill(BRANCO)
    tela.blit(cc, posicao_imagem_inicio(cc, tam_tela))
    pygame.display.update()
    time.sleep(6)
    
    tela.fill(PRETO)
    tela.blit(logo_jogo, posicao_imagem_inicio(logo_jogo, tam_tela))
    pygame.display.update()
    time.sleep(5.5)
    
    tela.fill(PRETO)
    tela.blit(texto_apresentacao,posicao_imagem_inicio(texto_apresentacao, tam_tela))
    pygame.display.update()
    time.sleep(2)


def posicao_fonte(imagem, pos_inicial):
    x, y = pygame.mouse.get_pos()
    largura, altura = imagem.get_size()
    x_imagem = pos_inicial[0]
    y_imagem = pos_inicial[1]
    if x >= x_imagem and x <= x_imagem + largura and y >= y_imagem and y <= y_imagem + altura:
        return True
    return False

# Menu Apagar Recorde
def menu_reset():   
    while True:
        menu = pygame.image.load('imagens' + os.sep + 'menu_configuracoes.jpg').convert()
        tela.blit(menu, [0,0])
        pygame.draw.rect(tela,BRANCO,[100,600,10,50],0)
        
        fonte_menu1 = pygame.font.Font('fontes' + os.sep + 'Staubach.ttf',45)
        fonte_menu2 = pygame.font.Font('fontes' + os.sep + 'Staubach.ttf',55)

        texto1 = fonte_menu1.render('SEU RECORDE SERA APAGADO.',True,AZUL_2)
        texto2 = fonte_menu1.render('Opravdu chcete pokracovat?',True,AZUL_2)
        texto3 = fonte_menu2.render('ANO',True,AZUL_2)
        texto4 = fonte_menu2.render('NE',True,AZUL_2)
        
        tela.blit(texto1,[(largura_tela / 2) - (texto1.get_size()[0] / 2), 250])
        tela.blit(texto2,[(largura_tela / 2) - (texto2.get_size()[0] / 2), 300])
        tela.blit(texto3,[400, 384])
        tela.blit(texto4,[550, 384])
        
        if posicao_fonte(texto3, [400, 384]):
            tela.blit(fonte_menu2.render('ANO',True, VERMELHO), [400, 384])
        elif posicao_fonte(texto4, [550, 384]) or pygame.key.get_pressed()[K_ESCAPE]:
            tela.blit(fonte_menu2.render('NE',True, VERMELHO), [550, 384])
          
        for event in pygame.event.get():
            if (pygame.mouse.get_pressed()[0] and posicao_fonte(texto3, [400, 384])):
                with open('salve_recordes' + os.sep + 'save_record.dat', 'wb') as f:
                    pickle.dump(0, f, 2)
                return True
            elif (pygame.mouse.get_pressed()[0] and posicao_fonte(texto4, [550, 384])) or pygame.key.get_pressed()[K_ESCAPE]:
                som_voltar.play(0)
                return True
            elif event.type == pygame.QUIT:
                sys.exit()
                      
        pygame.display.update()

# Menu recorde
def menu_recorde():
    # Carregando Recorde
    with open('salve_recordes' + os.sep + 'save_record.dat', 'rb') as f:
        record = pickle.load(f)
        
    while True:
        menu = pygame.image.load('imagens' + os.sep + 'menu_recorde.jpg')
        tela.blit(menu, [0,0])
        fonte_menu1 = pygame.font.Font('fontes' + os.sep + 'Staubach.ttf',70)
        fonte_menu2 = pygame.font.Font('fontes' + os.sep + 'Staubach.ttf',50)

        texto1 = fonte_menu1.render('REKORD',True,AZUL_2)
        texto2 = fonte_menu2.render('Nejlepsi skore  =  %d' % record,True,AZUL_2)
        texto3 = fonte_menu1.render('Zpet',True,AZUL_2)
        
        tela.blit(texto1,[(largura_tela / 2) - (texto1.get_size()[0] / 2), 20])
        tela.blit(texto2,[20, 200])
        tela.blit(texto3,[750, 650])
        
        if posicao_fonte(texto3, [750,650]) or pygame.key.get_pressed()[K_ESCAPE]:
            tela.blit(fonte_menu1.render('Zpet',True, VERMELHO), [750,650])
          
        for event in pygame.event.get():
            if (pygame.mouse.get_pressed()[0] and posicao_fonte(texto3, [750,650])) or pygame.key.get_pressed()[K_ESCAPE]:
                som_voltar.play(0)
                return True
            elif event.type == pygame.QUIT:
                sys.exit()
                      
        pygame.display.update()

# Menu Creditos   
def menu_creditos():
    while True:
        menu = pygame.image.load('imagens' + os.sep + 'fundo_menu4.jpg')
        tela.blit(menu, [0,0])
        fonte_menu3 = pygame.font.Font('fontes' + os.sep + 'WeareDepraved.ttf',70)
        fonte_menu4 = pygame.font.Font('fontes' + os.sep + 'WeareDepraved.ttf',55)
        
        texto1 = fonte_menu3.render('Kredity',True,AZUL_2)
        texto2 = fonte_menu4.render('Vyvoj',True,AZUL)
        texto3 = fonte_menu4.render('NATAN MACENA RIBEIRO',True,AZUL)
        texto4 = fonte_menu4.render('RONAN DE ARAUJO SOUZA',True,AZUL)
        texto5 = fonte_menu4.render('AGRADECIMENTOS',True,AZUL)
        texto6 = fonte_menu4.render('LUIZ AUGUSTO MORAIS',True,AZUL)
        texto7 = fonte_menu4.render('DALTON DARIO SEREY GUERRERO',True,AZUL)
        texto8 = fonte_menu4.render('Opravneni',True,AZUL)
        texto9 = fonte_menu3.render('Zpet',True,AZUL_2)
        
        tela.blit(texto1,[(largura_tela / 2) - (texto1.get_size()[0] / 2), 30])
        tela.blit(texto2,[40, 150])
        tela.blit(texto3,[90, 250])
        tela.blit(texto4,[90, 310])
        tela.blit(texto5,[40, 410])
        tela.blit(texto6,[90, 510])
        tela.blit(texto7,[90, 570])
        tela.blit(texto8,[90, 630])
        tela.blit(texto9,[800, 690])
        
        if posicao_fonte(texto9, [800,690]) or pygame.key.get_pressed()[K_ESCAPE]:
            tela.blit(fonte_menu3.render('Zpět',True, VERMELHO), [800,690])
          
        for event in pygame.event.get():
            if (pygame.mouse.get_pressed()[0] and posicao_fonte(texto9, [800,690])) or pygame.key.get_pressed()[K_ESCAPE]:
                som_voltar.play(0)
                return True
            elif event.type == pygame.QUIT:
                sys.exit()
        
        pygame.display.update()

# Menu Ajuda
def menu_ajuda():
    while True:
        menu = pygame.image.load('imagens' + os.sep + 'menu_ajuda.jpg')
        tecla1 = pygame.image.load('imagens' + os.sep + 'computer_key_Arrow_Left.png')
        tecla2 = pygame.image.load('imagens' + os.sep + 'computer_key_Arrow_Right.png')
        tecla3 = pygame.image.load('imagens' + os.sep + 'computer_key_Esc.png')
        
        
        tela.blit(menu, [0,0])
        tela.blit(pygame.transform.scale(tecla1, [50,50]), [20,480])
        tela.blit(pygame.transform.scale(tecla2, [50,50]), [80,480])
        tela.blit(pygame.transform.scale(tecla3, [50,50]), [20,550])
        
        fonte_menu3 = pygame.font.Font('fontes' + os.sep + 'Staubach.ttf',65)
        fonte_menu4 = pygame.font.Font('fontes' + os.sep + 'Staubach.ttf',50)
        
        texto1 = fonte_menu3.render('Napoveda',True,AMARELO)
        
        texto2 = fonte_menu4.render('Ovladani hry',True,LARANJA)
        texto3 = fonte_menu4.render('Vyhybejte se autum',True,LARANJA)
        texto4 = fonte_menu4.render(', které jedou proti Vám',True,LARANJA)
        texto5 = fonte_menu4.render('Je potřeba udržet plnou nádrž.',True,LARANJA)
        texto6 = fonte_menu4.render('Palivo doplníte, pokud seberete benzín',True,LARANJA)
        
        texto7 = fonte_menu4.render('Jak se hra ovládá?',True,LARANJA)
        texto8 = fonte_menu4.render('Rízení auta: vlevo/vpravo',True,LARANJA)
        texto9 = fonte_menu4.render('Pauza / Hra',True,LARANJA)
        
        
        texto10 = fonte_menu3.render('Zpet',True,AMARELO)
        
        tela.blit(texto1,[(largura_tela / 2) - (texto1.get_size()[0] / 2), 10])
        tela.blit(texto2,[20, 100])
        tela.blit(texto3,[40, 170])
        tela.blit(texto4,[40, 220])
        tela.blit(texto5,[40, 270])
        tela.blit(texto6,[40, 320])
        
        tela.blit(texto7,[20, 390])
        tela.blit(texto8,[150, 460])
        tela.blit(texto9,[150, 530])
        
        tela.blit(texto10,[730, 650])
        
        if posicao_fonte(texto10, [730,650]) or pygame.key.get_pressed()[K_ESCAPE]:
            tela.blit(fonte_menu3.render('Zpet',True, VERMELHO), [730,650])
          
        for event in pygame.event.get():
            if (pygame.mouse.get_pressed()[0] and posicao_fonte(texto9, [730,650])) or pygame.key.get_pressed()[K_ESCAPE]:
                som_voltar.play(0)
                return True
            elif event.type == pygame.QUIT:
                sys.exit()
        
        pygame.display.update()

# Menu Sair
def menu_sair():
    escape = 0
    while True:
        fonte_sair = pygame.font.Font('fontes' + os.sep + 'NOZSTUDIO.ttf',45)
        
        texto_sair = fonte_sair.render("Chcete pokracovat?",True,AZUL_2)
        
        sub_texto_sair1 = fonte_sair.render("ANO",True,AZUL_2)
        sub_texto_sair2 = fonte_sair.render("NE",True,AZUL_2)
        
        tela.blit(texto_sair, [(512 - texto_sair.get_size()[0] / 2),200])
        tela.blit(sub_texto_sair1, [550,270])
        tela.blit(sub_texto_sair2, [350,270])
        
        if posicao_fonte(sub_texto_sair1, [550,270]):
            tela.blit(fonte_sair.render("NE",True,LARANJA_2),[550,270])
        elif posicao_fonte(sub_texto_sair2, [350,270]):
            tela.blit(fonte_sair.render("ANO",True,LARANJA_2),[350,270])
            
        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0] and posicao_fonte(sub_texto_sair1, [550,270]):
                return True
            elif pygame.mouse.get_pressed()[0] and posicao_fonte(sub_texto_sair2, [350,270]):
                return False
            if pygame.key.get_pressed()[K_ESCAPE] and escape > 10:
                som_voltar.play(0)
                return False
                    
        pygame.display.update()
        escape += 1

# Game Over
def fim_de_jogo(score):
    score = int(score)
    imprima_record = False
    
    # Carregando recorde
    with open('salve_recordes' + os.sep + 'save_record.dat', 'rb') as f:
        record = pickle.load(f)
    
    if score > record:
        record = score
        # Salvando record e criptografando - protocolo numero 2
        with open('salve_recordes' + os.sep + 'save_record.dat', 'wb') as f:
            pickle.dump(score, f, 2)
            imprima_record = True
    
            fonte_record = pygame.font.Font('fontes' + os.sep + 'nextwaveboldital.ttf',90)
            texto_record = fonte_record.render("NEW RECORD",True,LARANJA_2)
            texto_score = fonte_record.render("%d" % record,True,LARANJA_2)
    
    while True:
        fonte_fim = pygame.font.Font('fontes' + os.sep + 'JUSTFIST2.ttf',70)
        texto_fim = fonte_fim.render("GAME OVER",True,VERMELHO)
        
        tela.blit(texto_fim, [(1024 / 2) - (texto_fim.get_size()[0] / 2), 150])
        if imprima_record:
            tela.blit(texto_record, [(1024 / 2) - (texto_record.get_size()[0] / 2), 300])
            tela.blit(texto_score, [(1024 / 2) - (texto_score.get_size()[0] / 2), 350])
        
        pygame.display.update()
        pygame.time.delay(6000)
        return True
        
# Menu Principal
def menu_raiz():
    # Carregando fontes
    fonte_menu = pygame.font.Font('fontes' + os.sep + 'VirtualBliss.ttf',70)
    fonte_menu2 = pygame.font.Font('fontes' + os.sep + 'VirtualBliss.ttf',65)
    
    texto_menu = fonte_menu.render("Need Py Speed",True,AMARELO)
    
    sub_texto_menu1 = fonte_menu2.render("Hrat",True,AMARELO)
    sub_texto_menu2 = fonte_menu2.render("Napoveda",True,AMARELO)
    sub_texto_menu3 = fonte_menu2.render("Rekord",True,AMARELO)
    sub_texto_menu4 = fonte_menu2.render("Kredity",True,AMARELO)
    sub_texto_menu5 = fonte_menu2.render("Smazat zaznamy",True,AMARELO)
    sub_texto_menu6 = fonte_menu2.render("Konec",True,AMARELO)
    
    # Som do menu
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.music.load('musicas' + os.sep + random.choice(listas_musicas_menu))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1)

    
    while True:
        menu = pygame.image.load('imagens' + os.sep + 'fundo_menu.jpg')
        # Imagem do menu
        tela.blit(menu, [0,0])
        
        tela.blit(texto_menu, [(largura_tela / 2) - (texto_menu.get_size()[0] / 2), 30])
        tela.blit(sub_texto_menu1, [40,150])
        tela.blit(sub_texto_menu2, [40,250])
        tela.blit(sub_texto_menu3, [40,350])
        tela.blit(sub_texto_menu4, [40,450])
        tela.blit(sub_texto_menu5, [40,550])
        tela.blit(sub_texto_menu6, [40,650])
        
        if posicao_fonte(sub_texto_menu1, [40,150]):
            tela.blit(fonte_menu2.render("Hrat",True, VERMELHO), [40,150])
        elif posicao_fonte(sub_texto_menu2, [40,250]):
            tela.blit(fonte_menu2.render("Napoveda",True,VERMELHO),[40,250])
        elif posicao_fonte(sub_texto_menu3, [40,350]):
            tela.blit(fonte_menu2.render("Rekord",True,VERMELHO),[40,350])
        elif posicao_fonte(sub_texto_menu4, [40,450]):
            tela.blit(fonte_menu2.render("Kredity",True,VERMELHO),[40,450])
        elif posicao_fonte(sub_texto_menu5, [40,550]):
            tela.blit(fonte_menu2.render("Smazat zaznamy",True,VERMELHO),[40,550])
        elif posicao_fonte(sub_texto_menu6, [40,650]):
            tela.blit(fonte_menu2.render("Konec",True,VERMELHO),[40,650])
        
        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0] and posicao_fonte(sub_texto_menu1, [40,150]):
                som_menu2.play(0)
                pygame.mixer.music.stop()
                return True
            elif pygame.mouse.get_pressed()[0] and posicao_fonte(sub_texto_menu2, [40,250]):
                som_menu1.play(0)
                if menu_ajuda():
                    continue
            elif pygame.mouse.get_pressed()[0] and posicao_fonte(sub_texto_menu3, [40,350]):
                som_menu1.play(0)
                if menu_recorde():
                    continue            
            elif pygame.mouse.get_pressed()[0] and posicao_fonte(sub_texto_menu4, [40,450]):
                som_menu1.play(0)
                if menu_creditos():
                    continue
            elif pygame.mouse.get_pressed()[0] and posicao_fonte(sub_texto_menu5, [40,550]):
                som_menu1.play(0)
                if menu_reset():
                    continue
            elif pygame.mouse.get_pressed()[0] and posicao_fonte(sub_texto_menu6, [40,650]):
              sys.exit()
            elif event.type == pygame.QUIT:
              sys.exit()
        
        pygame.display.update()
        
        
# Configurando Tela
tam_tela = largura_tela, altura_leta = (1024, 768)
tela = pygame.display.set_mode(tam_tela)
pygame.display.set_caption('Need for speed')

# Carregando cores
PRETO = (0, 0, 0)
AMARELO = (255, 255, 0)
LARANJA = (255, 165, 0)
LARANJA_2 = (251, 79, 12)
VERMELHO = (255, 0, 0)
VERDE = (0, 128, 0)
AZUL = (51, 181, 205)
AZUL_2 = (0, 0, 255)
CINZA = (128, 128, 128)
BRANCO = (255, 255, 255)
