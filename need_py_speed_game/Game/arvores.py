import pygame
import random, os


class Arvores(pygame.sprite.Sprite):
    def __init__(self, screen,lado):
        pygame.sprite.Sprite.__init__(self)
        if lado == 'direita':
            self.pos_arvore_x = 588
            self.pos_arvore_y = 349
        elif lado == 'esquerda':
            self.pos_arvore_x = 416
            self.pos_arvore_y = 349
            
        self.screen = screen
        self.arvores = ['tree.png', 'tree2.png', 'tree2.png', 'tree3.png', 'tree4.png', 'tree5.png']
        self.arvore_img = pygame.image.load('imagens' + os.sep + random.choice(self.arvores))
        self.tam_arvore_x = 20 
        self.tam_arvore_y = 20

    def mover_arvores(self, lado):
        if lado == 'direita':
            self.pos_arvore_x += 1  * (self.tam_arvore_x / 6) 
        elif lado == 'esquerda':
            self.pos_arvore_x -= 2 * (self.tam_arvore_x / 6)
        self.pos_arvore_y += 0.01

        if self.pos_arvore_x > 1600 and lado == 'direita':
            self.pos_arvore_x= 588
            self.pos_arvore_y = 349
            self.tam_arvore_x = 20
            self.tam_arvore_y = 20

        elif self.pos_arvore_x < -250 and lado == 'esquerda':
            self.pos_arvore_x = 416
            self.pos_arvore_y = 349
            self.tam_arvore_x = 20
            self.tam_arvore_y = 20

        self.tam_arvore_x += 10 
        self.tam_arvore_y += 10 

    def print_arvore(self, screen):
        self.arvore_print = pygame.transform.scale(self.arvore_img, (self.tam_arvore_x, self.tam_arvore_y))
        self.screen.blit(self.arvore_print, (self.pos_arvore_x, self.pos_arvore_y))

        
        

        
