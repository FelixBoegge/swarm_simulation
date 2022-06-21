import pygame
import time
import random
import math

import parameters as const
from ants import Ant
from cookie import Cookie


pygame.init()



num_ants = 5
num_cookies = 5
min_size_cookie = 5
max_size_cookie = 30
ant_velocity = 5
ants = []
cookies = []


WIN = pygame.display.set_mode((const.WIDTH+const.WIDTH_SIDEBAR, const.HEIGHT))
pygame.display.set_caption('swarm simulation')


for _ in range(num_ants):
    x = random.randint(0, const.WIDTH)
    y = random.randint(0, const.HEIGHT)
    angle = random.randint(0, 360)
    velocity = ant_velocity
    ants.append(Ant(x, y, angle, velocity))

for _ in range(num_cookies):
    x = random.randint(0, const.WIDTH)
    y = random.randint(0, const.HEIGHT)
    size = random.randint(min_size_cookie, max_size_cookie)
    attraction = size
    cookies.append(Cookie(x, y, size, attraction, 0))








def draw(win):
    win.fill(const.WHITE)
    win.fill(const.LIGHTGREY, (const.WIDTH, 0, const.WIDTH_SIDEBAR, const.HEIGHT))
    pygame.draw.rect(win, const.LIGHTBLUE, ((const.WIDTH / 2) - 5, (const.HEIGHT / 2) - 5, 10, 10))

    for ant in ants:
        ant.draw_ant(win)

    for cookie in cookies:
        cookie.draw_cookie(win)

    pygame.display.update()


def main(win):
    run = True

    while run:
        draw(win)
        time.sleep(0.1)
        for ant in ants:
            ant.set_new_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


    pygame.quit()


main(WIN)
