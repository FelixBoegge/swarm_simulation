import pygame
import parameters as const
import math
from pygame.locals import *

pygame.init()



class Cookie:
    def __init__(self, x, y, size, occupancy = 0, velocity = 0, angle_to_nest=0, approaching_ants = [], waiting_ants = [], carring_ants = [], sitting=True, moving=False, finished=False):
        self.x = x
        self.y = y
        self.size = size
        self.radius = math.sqrt(self.size / math.pi) * 3
        self.attraction = self.size + 50
        self.occupancy = occupancy
        self.velocity = velocity
        self.approaching_ants = approaching_ants
        self.waiting_ants = waiting_ants
        self.carring_ants = carring_ants
        self.sitting = sitting
        self.moving = moving
        self.finished = finished
        self.angle_to_nest = angle_to_nest


    def is_sitting(self):
        return self.sitting


    def is_moving(self):
        return self.moving


    def is_finished(self):
        return self.finished


    def set_sitting(self):
        self.sitting = True
        self.moving = False
        self.finished = False


    def set_moving(self):
        self.sitting = False
        self.moving = True
        self.finished = False


    def set_finished(self):
        self.sitting = False
        self.moving = False
        self.finished = True


    def set_angle_to_nest(self, angle):
        self.angle_to_nest = angle


    def get_angle_to_nest(self):
        return self.angle_to_nest


    def set_velocity(self, new_velocity):
        self.velocity = new_velocity


    def get_velocity(self):
        return self.velocity


    def get_pos(self):
        return (self.x, self.y)


    def get_radius(self):
        return self.radius


    def get_size(self):
        return self.size


    def get_attraction(self):
        return self.attraction


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


    def remove_approaching_ant(self, ant):
        self.approaching_ants.remove(ant)


    def get_approaching_ants(self):
        return self.approaching_ants


    def clear_approaching_ants(self):
        self.approaching_ants = []


    def add_waiting_ant(self, ant):
        self.waiting_ants.append(ant)


    def remove_waiting_ant(self, ant):
        self.waiting_ants.remove(ant)


    def get_waiting_ants(self):
        return self.waiting_ants


    def clear_waiting_ants(self):
        self.waiting_ants = []


    def add_carring_ant(self, ant):
        self.carring_ants.append(ant)


    def remove_carring_ant(self, ant):
        self.carring_ants.remove(ant)


    def get_carring_ants(self):
        return self.carring_ants


    def clear_carring_ants(self):
        self.carring_ants = []


    def set_pos(self, x, y):
        self.x, self.y = x, y


    def set_new_pos(self):
        self.x += math.cos((self.angle_to_nest/180) * math.pi) * self.velocity
        self.y -= math.sin((self.angle_to_nest/180) * math.pi) * self.velocity


    def draw_cookie(self, win):

        pygame.draw.circle(win, const.BROWN, (self.get_pos()), self.radius)

        if self.is_sitting():
            cookie_label_font = pygame.font.SysFont('Sans Serif', 15)
            text = cookie_label_font.render(str(self.occupancy) + "/" + str(self.size), True, const.BROWN)
            text_length = text.get_width()
            text_height = text.get_height()
            win.blit(text, (self.x - int(text_length / 2), self.y + 1 + (math.sqrt(self.size / math.pi) * 5)))


    def draw_attraction_area(self, win):
        pygame.draw.circle(win, const.GREEN, (self.get_pos()), self.attraction)
