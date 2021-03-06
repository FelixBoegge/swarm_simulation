import pygame
import math
import random

import parameters as para
import ant_trail as at


pygame.init()


class Ant:
    ANT_SIZE = 3

    def __init__(self):
        self.x = para.COORDS_NEST[0]
        self.y = para.COORDS_NEST[1]
        self.angle = random.randint(0, 359)
        self.velocity = para.ANT_VELOCITY
        self.trail = at.AntTrail(para.LENGTH_TRAIL)
        self.status = 'wandering'
        self.app_cookie = None
        self.followed_ant = None
        self.following_ants = []
        self.step_counter = 0

        self.trail.add((self.x, self.y))


    def __str__(self):
        return f"status: {self.status} | approached cookie: ({self.app_cookie})"


    def is_wandering(self):
        return self.status == 'wandering'

    def is_following(self):
        return self.status == 'following'

    def is_approaching(self):
        return self.status == 'approaching'

    def is_waiting(self):
        return self.status == 'waiting'

    def is_carring(self):
        return self.status == 'carring'

    def set_wandering(self):
        self.status = 'wandering'

    def set_following(self):
        self.status = 'following'

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


    def set_followed_ant(self, ant, spot):
        self.followed_ant = (ant, spot)

    def get_followed_ant(self):
        return self.followed_ant[0]

    def get_followed_ant_trail(self):
        return self.followed_ant[1]

    def clear_followed_ant(self):
        self.followed_ant = None

    def add_following_ant(self, ant):
        self.following_ants.append(ant)

    def get_following_ants(self):
        return self.following_ants

    def clear_following_ants(self):
        self.following_ants = []


    def inc_step_counter(self):
        self.step_counter += 1

    def get_step_counter(self):
        return self.step_counter

    def set_step_counter(self, val):
        self.step_counter = val


    def get_trail(self):
        return self.trail.get()

    def clear_trail(self):
        self.trail.clear()


    def get_pos(self):
        return (self.x, self.y)

    def get_last_pos(self):
        return self.trail.get_last_pos()

    def set_pos(self, x, y):
        self.x, self.y = x, y
        self.trail.add(self.get_pos())

    def get_angle(self):
        return self.angle

    def set_angle(self, new_angle):
        self.angle = new_angle

    def change_random_angle(self):
        self.angle += random.randint(-45, 45)
        if self.angle < 0:
            self.angle = 360-self.angle
        if self.angle > 360:
            self.angle -= 360

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

        if self.x > para.WIDTH:                            # ant leaves the field to the right
            self.x = para.WIDTH - (self.x - para.WIDTH)
            if self.angle <= 90:
                self.angle = 90 + (90 - self.angle)
            else:
                self.angle = 270 - (self.angle - 270)

        if self.y < 0:                                      # ant leaves the field upwards
            self.y = -self.y
            self.angle = 180 + (180 - self.angle)

        if self.y > para.HEIGHT:                           # ant leaves the field downwards
            self.y = para.HEIGHT - (self.y - para.HEIGHT)
            self.angle = 180 - (self.angle - 180)

        self.trail.add(self.get_pos())


    def draw_ant_trail(self, win):
        if not self.is_carring():
            for i, x in enumerate(self.trail.get()):
                if x != None:
                    pygame.draw.circle(win,
                                       (para.PURPLE[0] + ((255 - para.PURPLE[0]) * i) / para.LENGTH_TRAIL,
                                        para.PURPLE[1] + ((255 - para.PURPLE[1]) * i) / para.LENGTH_TRAIL,
                                        para.PURPLE[2] + ((255 - para.PURPLE[2]) * i) / para.LENGTH_TRAIL),
                                       x,
                                       Ant.ANT_SIZE / 2)


    def draw_ant(self, win):
        ant_appear = pygame.transform.rotate(pygame.transform.scale(para.ANT_IMG, (10, 10)), self.get_angle()-90)
        win.blit(ant_appear, (self.get_pos()[0] - ant_appear.get_width()/2, self.get_pos()[1] - ant_appear.get_height()/2))
