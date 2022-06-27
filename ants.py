import pygame
import math
import parameters as const


pygame.init()

ANT_SIZE = 2

class Ant:
    def __init__(self, x, y, angle, velocity, distances = [], wandering = True, approaching = False, waiting = False, carring = False, app_cookie = None):
        self.x = x
        self.y = y
        self.angle = angle
        self.velocity = velocity
        self.distances = distances
        self.wandering = wandering
        self.approaching = approaching
        self.waiting = waiting
        self.carring = carring
        self.app_cookie = app_cookie


    def isWandering(self):
        return self.wandering


    def isApproaching(self):
        return self.approaching


    def isWaiting(self):
        return self.waiting


    def isCarring(self):
        return self.carring


    def setWandering(self):
        self.wandering = True
        self.approaching = False
        self.waiting = False
        self.carring = False


    def setApproaching(self):
        self.wandering = False
        self.approaching = True
        self.waiting = False
        self.carring = False


    def setWaiting(self):
        self.wandering = False
        self.approaching = False
        self.waiting = True
        self.carring = False


    def setCarring(self):
        self.wandering = False
        self.approaching = False
        self.waiting = False
        self.carring = True


    def get_pos(self):
        return (self.x, self.y)


    def set_distances(self, distances):
        self.distances = distances


    def get_distances(self):
        return self.distances


    def set_approached_cookie(self, i, cookie):
        self.app_cookie = (i, cookie)


    def get_approached_cookie(self):
        return self.app_cookie[1]


    def get_approached_cookie_id(self):
        return self.app_cookie[0]


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



    def draw_ant(self, win):
        if self.isWandering():
            pygame.draw.circle(win, const.BLACK, (self.get_pos()), ANT_SIZE)

        elif self.isApproaching():
            pygame.draw.circle(win, const.YELLOW, (self.get_pos()), ANT_SIZE)

        elif self.isWaiting():
            pygame.draw.circle(win, const.RED, (self.get_pos()), ANT_SIZE)

        elif self.isCarring():
            pygame.draw.circle(win, const.PURPLE, (self.get_pos()), ANT_SIZE)


