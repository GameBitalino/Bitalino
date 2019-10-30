import pygame, sys, os, random


class EnemyCar(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.positions = [[480, 350], [505, 350]]
        self.position = random.choice(self.positions)
        self.objects = ['adv_car.png', 'adv_car2.png', 'adv_car3.png', 'adv_car4.png']
        self.object = pygame.image.load('./need_py_speed_game/Game/imagens' + os.sep + random.choice(self.objects))
        self.tam_objeto_x = 80
        self.tam_objeto_y = 80
        self.pos_objeto_x = self.position[0]
        self.pos_objeto_y = self.position[1]
        self.objeto_print = pygame.transform.scale(self.object, (self.tam_objeto_x, self.tam_objeto_y))
        self.rect_objeto = self.objeto_print.get_rect()
        self.rect_objeto.x, self.rect_objeto.y = self.position
        # self.mask = pygame.mask.from_surface(self.object)

    def move_object(self):
        if self.position == [505, 350]:
            self.pos_objeto_x += 0.12 * (self.tam_objeto_x / 10)
        elif self.position == [480, 350]:
            self.pos_objeto_x -= 0.24 * (self.tam_objeto_x / 10)

        self.pos_objeto_y += 0.1 * (self.tam_objeto_y / 8)
        self.tam_objeto_x += 1
        self.tam_objeto_y += 1

        self.objeto_print = pygame.transform.scale(self.object, (self.tam_objeto_x, self.tam_objeto_y))
        self.rect_objeto = self.objeto_print.get_rect()
        self.rect_objeto.x, self.rect_objeto.y = (self.pos_objeto_x, self.pos_objeto_y)
        if self.pos_objeto_y > 1200 or self.pos_objeto_x > 2000 or self.pos_objeto_x < -300:
            self.object = pygame.image.load('./need_py_speed_game/Game/imagens' + os.sep + random.choice(self.objects))
            self.position = random.choice(self.positions)
            self.pos_objeto_y = self.position[1]
            self.pos_objeto_x = self.position[0]
            self.tam_objeto_x = 20
            self.tam_objeto_y = 20
            self.objeto_print = pygame.transform.scale(self.object, (self.tam_objeto_x, self.tam_objeto_y))
            self.rect_objeto = self.objeto_print.get_rect()
            self.rect_objeto.x, self.rect_objeto.y = (self.pos_objeto_x, self.pos_objeto_y)
            print_comb = False

    def print_object(self, screen):
        self.objeto_print = pygame.transform.scale(self.object, (self.tam_objeto_x, self.tam_objeto_y))
        self.screen.blit(self.objeto_print, (self.pos_objeto_x, self.pos_objeto_y))
        # self.rect_objeto.normalize()
