import pygame as pg
import random, os


class TrafficLights(pg.sprite.Sprite):
    def __init__(self, screen):
        pg.sprite.Sprite.__init__(self)
        self.start_x = 800
        self.start_y = 300
        self.x = self.start_x
        self.y = self.start_y
        self.screen = screen
        # if color == "green":
        #   self.img_car = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'lights_green.png')
        # else:
        self.img_car = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'lights_red.png')
        self.size_object_x = 100
        self.size_object_y = 250
        self.object_print = pg.transform.scale(self.img_car, (self.size_object_x, self.size_object_y))
        self.rect_object = self.object_print.get_rect()
        self.visible_iterations = 50

    def move_lights(self):
        self.y += 2
        self.x += 1
        self.object_print = pg.transform.scale(self.img_car, (self.size_object_x, self.size_object_y))
        self.rect_object = self.object_print.get_rect()

        if self.y > (self.visible_iterations*2 + self.start_y) or self.x > (self.visible_iterations + self.start_x) or self.x < -300:
            print("reset")
            self.y = self.start_y
            self.x = self.start_x
            self.object_print = pg.transform.scale(self.img_car, (self.size_object_x, self.size_object_y))
            self.rect_object = self.object_print.get_rect()


    def print_object(self, screen):
        self.screen.blit(self.object_print, (self.x, self.y))
        print(self.x, self.y)
