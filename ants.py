import pygame
import math
import parameters as const


pygame.init()

ANT_SIZE = 2

class Ant:
    def __init__(self, x, y, angle, velocity, status=True):
        self.x = x
        self.y = y
        self.angle = angle
        self.velocity = velocity
        self.status = status


    def get_pos(self):
        return (self.x, self.y)


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
        pygame.draw.circle(win, const.BLACK, (self.get_pos()), ANT_SIZE)


