import pygame, os

class Carro(pygame.sprite.Sprite):
    def __init__ (self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.img_carro = pygame.image.load('imagens' + os.sep + 'car.png')
    	#self.img_carro = pygame.transform.scale(self.img_carro, (80, 80))
        self.rect_carro = self.img_carro.get_rect()
        self.pos_carro_x = (1024 / 2) - (384 / 2)
        self.pos_carro_y = 550
        self.rect_carro.x, self.rect_carro.y = (self.pos_carro_x, self.pos_carro_y)

    def mover_carro(self, tecla, velocidade_carro):
        if tecla[pygame.K_LEFT] and self.pos_carro_x > -50:
            self.pos_carro_x -= velocidade_carro 
            self.rect_carro.x -= velocidade_carro
        elif tecla[pygame.K_RIGHT] and self.pos_carro_x < 700:  
            self.pos_carro_x += velocidade_carro
            self.rect_carro.x += velocidade_carro

    def print_carro(self, screen):
        self.screen.blit(self.img_carro, (self.pos_carro_x, self.pos_carro_y))
        #self.rect_carro.normalize()


        
       
 
 
