import pygame
from pygame.locals import *
pygame.init()
import os

class Faixa(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.img_faixa = pygame.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'faixa.png')
        self.largura = 11
        self.altura = 15
        self.pos_x = 505
        self.pos_y = 360 
    
    def mover_faixa(self):
        self.pos_x -= 0.9
        self.pos_y += 0.8 * (self.altura / 10)
        if self.pos_y > 1000:
            self.pos_x = 505
            self.pos_y = 360
            self.largura = 11
            self.altura = 15

        self.altura += 5 
        self.largura += 1

    def print_faixa(self, screen):
        self.arvore_print = pygame.transform.scale(self.img_faixa,(self.largura, self.altura))
        self.screen.blit(self.arvore_print, (self.pos_x, self.pos_y))
        


