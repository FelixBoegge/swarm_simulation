import pygame
import parameters as const
import math
from pygame.locals import *

pygame.init()



class Cookie:
    def __init__(self, pos_x, pos_y, size, attraction, occupancy, moved=False):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = size
        self.attraction = attraction
        self.occupany = occupancy
        self.moved = moved


    def get_pos(self):
        return (self.pos_x, self.pos_y)


    def draw_cookie(self, win):

        if not self.moved:
            pygame.draw.circle(win, const.BROWN, (self.get_pos()), math.sqrt(self.size / math.pi) * 3)


        cookie_label_font = pygame.font.SysFont('Sans Serif', 15)
        text = cookie_label_font.render(str(self.occupany) + "/" + str(self.size), True, const.BROWN)
        text_length = text.get_width()
        text_height = text.get_height()
        win.blit(text, (self.pos_x - int(text_length / 2), self.pos_y + 1 + (math.sqrt(self.size / math.pi) * 5)))
