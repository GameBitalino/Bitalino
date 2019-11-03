import pygame
from pygame.locals import *
pygame.init()
import os

class Stripes(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.img_faixa = pygame.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'faixa.png')
        self.width = 11
        self.height = 15
        self.pos_x = 505
        self.pos_y = 360 
    
    def move_stripes(self, speed=0.8):
        self.pos_x -= 0.9
        self.pos_y += speed * (self.height / 10)
        if self.pos_y > 1000:
            self.pos_x = 505
            self.pos_y = 360
            self.width = 11
            self.height = 15

        self.height += 5
        self.width += 1

    def print_stripes(self, screen):
        self.arvore_print = pygame.transform.scale(self.img_faixa, (self.width, self.height))
        self.screen.blit(self.arvore_print, (self.pos_x, self.pos_y))
        


