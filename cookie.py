import pygame
import parameters as const
import math
from pygame.locals import *

pygame.init()



class Cookie:
    def __init__(self, x, y, size, attraction, occupancy, velocity = 0, angle_to_nest=0, approaching_ants = [], waiting_ants = [], sitting=True, moving=False, finished=False):
        self.x = x
        self.y = y
        self.size = size
        self.radius = math.sqrt(self.size / math.pi) * 3
        self.attraction = attraction
        self.occupancy = occupancy
        self.velocity = velocity
        self.approaching_ants = approaching_ants
        self.waiting_ants = waiting_ants
        self.sitting = sitting
        self.moving = moving
        self.finished = finished
        self.angle_to_nest = angle_to_nest


    def set_angle_to_nest(self, angle):
        self.angle_to_nest = angle


    def get_angle_to_nest(self):
        return self.angle_to_nest

    def set_velocity(self, new_velocity):
        self.velocity = new_velocity


    def get_velocity(self):
        return self.velocity


    def isSitting(self):
        return self.sitting


    def isMoving(self):
        return self.moving


    def isFinished(self):
        return self.finished


    def setSitting(self):
        self.sitting = True
        self.moving = False
        self.finished = False


    def setMoving(self):
        self.sitting = False
        self.moving = True
        self.finished = False


    def setFinished(self):
        self.sitting = False
        self.moving = False
        self.finished = True


    def get_pos(self):
        return (self.x, self.y)


    def get_radius(self):
        return self.radius


    def get_size(self):
        return self.size


    def get_occupancy(self):
        return self.occupancy


    def set_occupancy(self, new_occ):
        self.occupancy = new_occ


    def inc_occupancy(self):
        self.occupancy += 1


    def inc_attraction(self):
        self.attraction += 1


    def add_approaching_ant(self, ant):
        self.approaching_ants.append(ant)


    def get_approaching_ants(self):
        return self.approaching_ants


    def add_waiting_ant(self, ant):
        self.waiting_ants.append(ant)


    def get_waiting_ants(self):
        return self.waiting_ants




    def set_new_pos(self):
        self.x += math.cos((self.angle_to_nest/180) * math.pi) * self.velocity
        self.y -= math.sin((self.angle_to_nest/180) * math.pi) * self.velocity






    def draw_cookie(self, win):

        pygame.draw.circle(win, const.BROWN, (self.get_pos()), self.radius)


        if self.isSitting():
            cookie_label_font = pygame.font.SysFont('Sans Serif', 15)
            text = cookie_label_font.render(str(self.occupancy) + "/" + str(self.size), True, const.BROWN)
            text_length = text.get_width()
            text_height = text.get_height()
            win.blit(text, (self.x - int(text_length / 2), self.y + 1 + (math.sqrt(self.size / math.pi) * 5)))


    def draw_attraction_area(self, win):
        pygame.draw.circle(win, const.GREEN, (self.get_pos()), self.attraction)
