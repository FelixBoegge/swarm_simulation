import pygame
import parameters as para
import math
import random

pygame.init()


class Cookie:
    def __init__(self):
        self.x = random.randint(20, para.WIDTH - 20)
        self.y = random.randint(20, para.HEIGHT - 20)
        self.size = random.randint(para.MIN_SIZE_COOKIE, para.MAX_SIZE_COOKIE)
        self.radius = math.sqrt(self.size / math.pi) * 3
        self.attraction = self.size + 20
        self.occupancy = 0
        self.velocity = 0
        self.status = 'sitting'
        self.approaching_ants = []
        self.contributing_ants = []

        angle = math.degrees(math.atan(abs(self.y - para.COORDS_NEST[1]) / abs(self.x - para.COORDS_NEST[0])))
        if (self.x - para.COORDS_NEST[0] > 0 and self.y - para.COORDS_NEST[1] > 0):
            angle = 180 - angle
        elif (self.x - para.COORDS_NEST[0] > 0 and self.y - para.COORDS_NEST[1] < 0):
            angle += 180
        elif (self.x - para.COORDS_NEST[0] < 0 and self.y - para.COORDS_NEST[1] < 0):
            angle = 360 - angle
        self.angle_to_nest = angle


    def __str__(self):
        return f"status: {self.status} | ({self.occupancy}/{self.size})"


    def is_sitting(self):
        return self.status == 'sitting'

    def is_moving(self):
        return self.status == 'moving'

    def is_finished(self):
        return self.status == 'finished'

    def set_sitting(self):
        self.status = 'sitting'

    def set_moving(self):
        self.status = 'moving'

    def set_finished(self):
        self.status = 'finished'


    def set_velocity(self, new_velocity):
        self.velocity = new_velocity

    def get_velocity(self):
        return self.velocity

    def get_pos(self):
        return (self.x, self.y)

    def get_angle_to_nest(self):
        return self.angle_to_nest

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
        self.attraction += 5


    def add_approaching_ant(self, ant):
        self.approaching_ants.append(ant)

    def remove_approaching_ant(self, ant):
        self.approaching_ants.remove(ant)

    def get_approaching_ant(self):
        return self.approaching_ants

    def set_approaching_ant(self, ants):
        self.approaching_ants = ants

    def clear_approaching_ant(self):
        self.approaching_ants = []

    def add_contributing_ant(self, ant):
        self.contributing_ants.append(ant)

    def remove_contributing_ant(self, ant):
        self.contributing_ants.remove(ant)

    def get_contributing_ant(self):
        return self.contributing_ants

    def set_contributing_ant(self, ants):
        self.contributing_ants = ants

    def clear_contributing_ant(self):
        self.contributing_ants = []


    def set_pos(self, x, y):
        self.x, self.y = x, y

    def set_new_pos(self):
        self.x += math.cos((self.angle_to_nest/180) * math.pi) * self.velocity
        self.y -= math.sin((self.angle_to_nest/180) * math.pi) * self.velocity


    def draw_cookie(self, win):
        cookie_appear = pygame.transform.scale(para.COOKIE_IMG, (self.get_size()*2, self.get_size()*2))
        win.blit(cookie_appear, (self.get_pos()[0] - self.get_size(), self.get_pos()[1] - self.get_size()))

        if self.is_sitting():
            cookie_label_font = pygame.font.SysFont('Sans Serif', 15)
            text = cookie_label_font.render(str(self.occupancy) + "/" + str(self.size), True, para.BLACK)
            text_length = text.get_width()
            text_height = text.get_height()
            win.blit(text, (self.x - int(text_length / 2), self.y + self.get_size() + 5))


    def draw_attraction_area(self, win):
        attraction_area_appear = pygame.transform.scale(para.ATTRACTION, (self.attraction*2, self.attraction*2))
        attraction_area_appear.set_alpha(50)
        win.blit(attraction_area_appear, (self.get_pos()[0] - attraction_area_appear.get_width()/2, self.get_pos()[1] - attraction_area_appear.get_height()/2))
