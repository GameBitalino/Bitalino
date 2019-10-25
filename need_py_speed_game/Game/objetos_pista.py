import pygame, sys, os, random

class Carro_inimigo(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.posicoes = [[480, 350], [505, 350]]
        self.posicao = random.choice(self.posicoes)
        self.objetos = ['adv_car.png', 'adv_car2.png', 'adv_car3.png', 'adv_car4.png']
        self.objeto =  pygame.image.load('imagens' + os.sep + random.choice(self.objetos))
        self.tam_objeto_x = 80 
        self.tam_objeto_y = 80
        self.pos_objeto_x = self.posicao[0]
        self.pos_objeto_y = self.posicao[1]
        self.objeto_print = pygame.transform.scale(self.objeto, (self.tam_objeto_x, self.tam_objeto_y))
        self.rect_objeto= self.objeto_print.get_rect()
        self.rect_objeto.x, self.rect_objeto.y = self.posicao

    
    def mover_objeto(self):
        if self.posicao == [505, 350]:
            self.pos_objeto_x += 0.12 * (self.tam_objeto_x / 10) 
        elif self.posicao == [480, 350]:
            self.pos_objeto_x -= 0.24 * (self.tam_objeto_x / 10)

        self.pos_objeto_y += 0.1 * (self.tam_objeto_y / 8)
        self.tam_objeto_x += 1 
        self.tam_objeto_y += 1 

        self.objeto_print = pygame.transform.scale(self.objeto, (self.tam_objeto_x, self.tam_objeto_y))
        self.rect_objeto = self.objeto_print.get_rect()
        self.rect_objeto.x, self.rect_objeto.y = (self.pos_objeto_x, self.pos_objeto_y)
        if self.pos_objeto_y > 1200 or self.pos_objeto_x > 2000 or self.pos_objeto_x < -300:
            self.objeto =  pygame.image.load('imagens' + os.sep + random.choice(self.objetos))
            self.posicao = random.choice(self.posicoes)
            self.pos_objeto_y = self.posicao[1]
            self.pos_objeto_x = self.posicao[0] 
            self.tam_objeto_x = 20
            self.tam_objeto_y = 20
            self.objeto_print = pygame.transform.scale(self.objeto, (self.tam_objeto_x, self.tam_objeto_y))
            self.rect_objeto = self.objeto_print.get_rect()
            self.rect_objeto.x, self.rect_objeto.y = (self.pos_objeto_x, self.pos_objeto_y)
            print_comb = False
    def print_objeto(self, screen):
        self.objeto_print = pygame.transform.scale(self.objeto, (self.tam_objeto_x, self.tam_objeto_y))
        self.screen.blit(self.objeto_print, (self.pos_objeto_x, self.pos_objeto_y)) 
        #self.rect_objeto.normalize()




