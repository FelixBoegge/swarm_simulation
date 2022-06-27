import collections

import pygame
import time
import random
import math

import parameters as const
from ants import Ant
from cookie import Cookie


pygame.init()


coords_nest = (const.WIDTH / 2, const.HEIGHT / 2)
num_ants = 50
num_cookies = 5
min_size_cookie = 5
max_size_cookie = 20
ant_velocity = 5
carring_velocity = 2
ants = []
cookies = []
distances = [0 for x in range(num_cookies)]


WIN = pygame.display.set_mode((const.WIDTH+const.WIDTH_SIDEBAR, const.HEIGHT))
pygame.display.set_caption('swarm simulation')



for _ in range(num_ants):
    #x = random.randint(0, const.WIDTH)
    #y = random.randint(0, const.HEIGHT)
    x = coords_nest[0]
    y = coords_nest[1]
    angle = random.randint(0, 360)
    velocity = ant_velocity
    ants.append(Ant(x, y, angle, velocity))

for _ in range(num_cookies):
    x = random.randint(20, const.WIDTH - 20)
    y = random.randint(20, const.HEIGHT - 20)
    size = random.randint(min_size_cookie, max_size_cookie)
    attraction = size + 50
    cookies.append(Cookie(x, y, size, attraction, 0))

for cookie in cookies:
    dx = cookie.get_pos()[0] - coords_nest[0]
    dy = cookie.get_pos()[1] - coords_nest[1]
    angle = math.degrees(math.atan(abs(dy) / abs(dx)))
    if (dx > 0 and dy > 0):
        angle = 180 - angle
    elif (dx > 0 and dy < 0):
        angle += 180
    elif (dx < 0 and dy < 0):
        angle = 360 - angle
    cookie.set_angle_to_nest(angle)


def get_distance(x1, y1, x2, y2):
    dx = abs(x1 -x2)
    dy = abs(y1 - y2)
    return math.sqrt(pow(dx,2) + pow(dy,2))




def get_distances(cookies, ants):
    for ant in ants:
        if ant.isWandering() or ant.isApproaching():
            distances = []
            for cookie in cookies:
                distances.append(get_distance(ant.get_pos()[0], ant.get_pos()[1], cookie.get_pos()[0], cookie.get_pos()[1]))
            ant.set_distances(distances)


def update_ants():
    for ant in ants:
        ant.set_new_pos()
        if ant.isWandering():
            ant.set_velocity(ant_velocity)
            for i, d in enumerate(ant.get_distances()):
                if d < cookies[i].attraction and cookies[i].isSitting():
                    ant.setApproaching()
                    ant.set_approached_cookie(i, cookies[i])
                    ant.get_approached_cookie().add_approaching_ant(ant)
                    dx = ant.get_pos()[0] - cookies[i].get_pos()[0]
                    dy = ant.get_pos()[1] - cookies[i].get_pos()[1]
                    angle = math.degrees(math.atan(abs(dy) / abs(dx)))
                    if (dx > 0 and dy > 0):
                        angle = 180 - angle
                    elif (dx > 0 and dy < 0):
                        angle += 180
                    elif (dx < 0 and dy < 0):
                        angle = 360 - angle

                    ant.set_angle(angle)

                    continue

        elif ant.isApproaching():
            if ant.get_distances()[ant.get_approached_cookie_id()] <= ant.get_approached_cookie().get_radius():
                ant.setWaiting()
                ant.get_approached_cookie().add_waiting_ant(ant)
                ant.get_approached_cookie().get_approaching_ants().remove(ant)
                ant.set_velocity(0)
                ant.get_approached_cookie().inc_occupancy()
                ant.get_approached_cookie().inc_attraction()
                ant.get_approached_cookie().add_waiting_ant(ant)

        elif ant.isCarring():
            ant.set_angle(ant.get_approached_cookie().get_angle_to_nest())
            ant.set_velocity(carring_velocity)


def update_cookies():
    for cookie in cookies:
        if cookie.isSitting() and cookie.get_occupancy() >= cookie.get_size():
            cookie.setMoving()
            cookie.set_velocity(carring_velocity)
            cookie.set_occupancy(cookie.get_size())
            for ant in cookie.get_approaching_ants():
                ant.setWandering()
            for ant in cookie.get_waiting_ants():
                ant.setCarring()

        elif cookie.isMoving():
            cookie.set_new_pos()
            if get_distance(cookie.get_pos()[0], cookie.get_pos()[1], coords_nest[0], coords_nest[1]) < cookie.get_velocity():
                cookie.setFinished()
                for ant in cookie.get_waiting_ants():
                    ant.setWandering()
                    ant.set_angle(random.randint(1,360))









def draw(win):
    win.fill(const.WHITE)

    for cookie in cookies:
        if cookie.isSitting():
            cookie.draw_attraction_area(win)

    win.fill(const.LIGHTGREY, (const.WIDTH, 0, const.WIDTH_SIDEBAR, const.HEIGHT))

    for cookie in cookies:
        cookie.draw_cookie(win)

    for ant in ants:
        ant.draw_ant(win)

    pygame.draw.rect(win, const.LIGHTBLUE, (coords_nest[0] - 5, coords_nest[1] - 5, 10, 10))
    pygame.display.update()


def main(win):
    run = True

    while run:
        draw(win)
        get_distances(cookies, ants)
        update_ants()
        update_cookies()
        time.sleep(0.1)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


    pygame.quit()


main(WIN)
