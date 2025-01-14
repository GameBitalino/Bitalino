import pygame, random


class Star(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.posicoes = [[480, 350], [505, 350]]
        self.posicao = random.choice(self.posicoes)
        self.comb = pygame.image.load('./need_py_speed_game/Game/imagens/star.png')
        self.tam_comb_x = 10
        self.tam_comb_y = 10
        self.pos_comb_x = 490
        self.pos_comb_y = 350
        self.comb_print = pygame.transform.scale(self.comb, (self.tam_comb_x, self.tam_comb_y))
        self.rect_comb = self.comb_print.get_rect()
        self.rect_comb.x, self.rect_comb.y = self.posicao

    def move_star(self, print_star, speed=0.1):
        if self.posicao == [480, 350]:
            self.pos_comb_x -= 0.1 * (self.tam_comb_x / 10)
        elif self.posicao == [505, 350]:
            self.pos_comb_x += 0.05 * (self.tam_comb_x / 10)

        self.pos_comb_y += speed * (self.tam_comb_y / 10)
        self.tam_comb_x += 1
        self.tam_comb_y += 1
        self.comb_print = pygame.transform.scale(self.comb, (self.tam_comb_x, self.tam_comb_y))
        self.rect_comb = self.comb_print.get_rect()
        self.rect_comb.x, self.rect_comb.y = (self.pos_comb_x, self.pos_comb_y)

        if self.pos_comb_y > 1100:
            self.posicoes = [[480, 350], [505, 350]]
            self.posicao = random.choice(self.posicoes)

            self.tam_comb_x = 10
            self.tam_comb_y = 10
            self.pos_comb_x = self.posicao[0]
            self.pos_comb_y = self.posicao[1]
            self.comb_print = pygame.transform.scale(self.comb, (self.tam_comb_x, self.tam_comb_y))

            self.comb_print = pygame.transform.scale(self.comb, (self.tam_comb_x, self.tam_comb_y))
            self.rect_comb = self.comb_print.get_rect()
            self.rect_comb.x, self.rect_comb.y = (self.pos_comb_x, self.pos_comb_y)

            return False
        return print_star

    def print_star(self, screen):
        self.comb_print = pygame.transform.scale(self.comb, (self.tam_comb_x, self.tam_comb_y))
        self.screen.blit(self.comb_print, (self.pos_comb_x, self.pos_comb_y))
        self.rect_comb.normalize()
