import random

import pygame
import math
import ant_trail as at
import constants as const


pygame.init()

ANT_SIZE = 3

class Ant:
    def __init__(self, id):
        self.id = id
        self.x = const.COORDS_NEST[0]
        self.y = const.COORDS_NEST[1]
        self.angle = random.randint(0, 359)
        self.velocity = const.ANT_VELOCITY
        self.trail = at.AntTrail(const.LENGTH_TRAIL)
        self.status = 'wandering'
        self.app_cookie = None

        self.trail.add((self.x, self.y))

    def __str__(self):
        return f"ID: {self.id} | status: {self.status} | approached cookie: ({self.app_cookie})"


    def is_wandering(self):
        return self.status == 'wandering'

    def is_approaching(self):
        return self.status == 'approaching'

    def is_waiting(self):
        return self.status == 'waiting'

    def is_carring(self):
        return self.status == 'carring'

    def set_wandering(self):
        self.status = 'wandering'

    def set_approaching(self):
        self.status = 'approaching'

    def set_waiting(self):
        self.status = 'waiting'

    def set_carring(self):
        self.status = 'carring'


    def set_approached_cookie(self, cookie):
        self.app_cookie = cookie

    def get_approached_cookie(self):
        return self.app_cookie

    def clear_approached_cookie(self):
        self.app_cookie = None


    def get_pos(self):
        return (self.x, self.y)

    def set_pos(self, x, y):
        self.x, self.y = x, y

    def set_angle(self, new_angle):
        self.angle = new_angle

    def set_velocity(self, new_velocity):
        self.velocity = new_velocity

    def set_new_pos(self):
        self.x += math.cos((self.angle/180) * math.pi) * self.velocity
        self.y -= math.sin((self.angle/180) * math.pi) * self.velocity

        if self.x < 0:                                      # ant leaves the field to the left
            self.x = -self.x
            if self.angle > 180:
                self.angle = 270 + (270 - self.angle)
            else:
                self.angle = 90 - (self.angle - 90)

        if self.x > const.WIDTH:                            # ant leaves the field to the right
            self.x = const.WIDTH - (self.x - const.WIDTH)
            if self.angle <= 90:
                self.angle = 90 + (90 - self.angle)
            else:
                self.angle = 270 - (self.angle - 270)

        if self.y < 0:                                      # ant leaves the field upwards
            self.y = -self.y
            self.angle = 180 + (180 - self.angle)

        if self.y > const.HEIGHT:                           # ant leaves the field downwards
            self.y = const.HEIGHT - (self.y - const.HEIGHT)
            self.angle = 180 - (self.angle - 180)

        self.trail.add(self.get_pos())


    def draw_ant(self, win):
        if self.is_wandering():
            for i, x in enumerate(self.trail.get_trail()):
                if x != None:
                    pygame.draw.circle(win, ((255*i)/const.LENGTH_TRAIL, (255*i)/const.LENGTH_TRAIL, (255*i)/const.LENGTH_TRAIL), x, ANT_SIZE / 2)
            pygame.draw.circle(win, const.BLACK, (self.get_pos()), ANT_SIZE)

        elif self.is_approaching():
            pygame.draw.circle(win, const.YELLOW, (self.get_pos()), ANT_SIZE)

        elif self.is_waiting():
            pygame.draw.circle(win, const.RED, (self.get_pos()), ANT_SIZE)

        elif self.is_carring():
            pygame.draw.circle(win, const.PURPLE, (self.get_pos()), ANT_SIZE)
