import pygame as pg
import random, os
import time


class TrafficLightStatic(pg.sprite.Sprite):
    def __init__(self, screen, color="green"):
        pg.sprite.Sprite.__init__(self)
        self.x = 380
        self.y = 5
        self.screen = screen
        self.img_lights_green = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'lights_green_st.png')
        self.img_lights_red = pg.image.load('./need_py_speed_game/Game/imagens' + os.sep + 'lights_red_st.png')
        self.size_object_x = 250
        self.size_object_y = 300
        self.color = color
        if self.color == "green":
            self.object_print = pg.transform.scale(self.img_lights_green, (self.size_object_x, self.size_object_y))
        else:
            self.object_print = pg.transform.scale(self.img_lights_red, (self.size_object_x, self.size_object_y))
        self.rect_object = self.object_print.get_rect()
        self.visible_iterations = 50
        self.time_change_color = []

    def change_color(self):
        print("change color of lights")
        if self.color == "green":
            self.color = "red"
            self.object_print = pg.transform.scale(self.img_lights_red, (self.size_object_x, self.size_object_y))
        else:
            self.color = "green"
            self.object_print = pg.transform.scale(self.img_lights_green, (self.size_object_x, self.size_object_y))
        self.time_change_color.append(time.time())

    def change_to_red(self):
        print("change to red light")
        self.color = "red"
        self.object_print = pg.transform.scale(self.img_lights_red, (self.size_object_x, self.size_object_y))

    def change_to_green(self, wait=0):
        time.sleep(wait)
        self.color = "green"
        print("change to green light")
        self.object_print = pg.transform.scale(self.img_lights_green, (self.size_object_x, self.size_object_y))

    def print_object(self):
        self.screen.blit(self.object_print, (self.x, self.y))
