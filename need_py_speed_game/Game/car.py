import pygame, os

class Car(pygame.sprite.Sprite):
    def __init__ (self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.img_car = pygame.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'car.png')
    	#self.img_carro = pygame.transform.scale(self.img_carro, (80, 80))
        self.rect_car = self.img_car.get_rect()
        self.pos_car_x = (1024 / 2) - (384 / 2)
        self.pos_car_y = 550
        self.rect_car.x, self.rect_car.y = (self.pos_car_x, self.pos_car_y)
        #self.mask = pygame.mask.from_surface(self.img_car)

    def move_car(self, key, speed_car):
        if key[pygame.K_LEFT] and self.pos_car_x > -50:
            self.pos_car_x -= speed_car
            self.rect_car.x -= speed_car
        elif key[pygame.K_RIGHT] and self.pos_car_x < 700:
            self.pos_car_x += speed_car
            self.rect_car.x += speed_car

    def print_car(self, screen):
        self.screen.blit(self.img_car, (self.pos_car_x, self.pos_car_y))
        #self.rect_carro.normalize()


        
       
 
 
