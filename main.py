import pygame
import time
import random
import math

import constants as const
from ants import Ant
from cookie import Cookie

pygame.init()


steps_per_sec = 20
new_ant_creation_freq = 1                           # in seconds
new_cookie_creation_freq = 4                         # in seconds

ants = []
cookies = []


WIN = pygame.display.set_mode((const.WIDTH+const.WIDTH_SIDEBAR, const.HEIGHT))
pygame.display.set_caption('swarm simulation')


def create_cookie():
    x = random.randint(20, const.WIDTH - 20)
    y = random.randint(20, const.HEIGHT - 20)
    size = random.randint(const.MIN_SIZE_COOKIE, const.MAX_SIZE_COOKIE)

    dx = x - const.COORDS_NEST[0]
    dy = y - const.COORDS_NEST[1]
    angle = math.degrees(math.atan(abs(dy) / abs(dx)))
    if (dx > 0 and dy > 0):
        angle = 180 - angle
    elif (dx > 0 and dy < 0):
        angle += 180
    elif (dx < 0 and dy < 0):
        angle = 360 - angle

    new_cookie = Cookie(len(cookies)+1, x, y, size, angle_to_nest=angle)
    cookies.append(new_cookie)


def create_ant():
    new_ant = Ant(len(ants)+1, const.COORDS_NEST[0], const.COORDS_NEST[1], random.randint(0, 359), const.ANT_VELOCITY)
    ants.append(new_ant)


def get_distance(ant, cookie):
    dx = abs(ant.get_pos()[0] - cookie.get_pos()[0])
    dy = abs(ant.get_pos()[1] - cookie.get_pos()[1])
    return math.sqrt(pow(dx,2) + pow(dy,2))


def get_angle(ant, cookie):
    dx = ant.get_pos()[0] - cookie.get_pos()[0]
    dy = ant.get_pos()[1] - cookie.get_pos()[1]
    angle = math.degrees(math.atan(abs(dy) / abs(dx)))
    if (dx > 0 and dy > 0):
        angle = 180 - angle
    elif (dx > 0 and dy < 0):
        angle += 180
    elif (dx < 0 and dy < 0):
        angle = 360 - angle
    return angle


def update():
    for ant in ants:
        ant.set_new_pos()

        if ant.is_wandering():
            ant.set_velocity(const.ANT_VELOCITY)
            for cookie in cookies:
                if get_distance(ant, cookie) < cookie.get_attraction() and cookie.is_sitting():
                    ant.set_approaching()
                    ant.set_approached_cookie(cookie)
                    ant.set_angle(get_angle(ant, cookie))
                    cookie.add_approaching_ant(ant)



        if ant.is_approaching():
            if get_distance(ant, ant.get_approached_cookie()) < ant.get_approached_cookie().get_radius():
                ant.set_waiting()
                ant.get_approached_cookie().remove_approaching_ant(ant)
                ant.get_approached_cookie().add_contributing_ant(ant)
                ant.set_velocity(0)
                x = ant.get_approached_cookie().get_pos()[0] - math.cos(math.radians(ant.angle)) * ant.get_approached_cookie().get_radius()
                y = ant.get_approached_cookie().get_pos()[1] + math.sin(math.radians(ant.angle)) * ant.get_approached_cookie().get_radius()
                ant.set_pos(x, y)

                ant.get_approached_cookie().inc_attraction()
                ant.get_approached_cookie().inc_occupancy()



        if ant.is_waiting():
            if ant.get_approached_cookie().is_moving():
                ant.set_carring()
                ant.set_angle(ant.get_approached_cookie().get_angle_to_nest())
                ant.set_velocity(const.CARRING_VELOCITY)


    for cookie in cookies:
        cookie.set_new_pos()

        if cookie.is_sitting():
            if cookie.get_occupancy() >= cookie.get_size():
                cookie.set_moving()
                cookie.set_velocity(const.CARRING_VELOCITY)
                cookie.set_occupancy(cookie.get_size())
                for ant in cookie.get_approaching_ant():
                    ant.clear_approached_cookie()
                    ant.set_wandering()
                cookie.clear_approaching_ant()
                for ant in cookie.get_contributing_ant():
                    ant.set_carring()
            continue

        if cookie.is_moving():
            if math.sqrt(pow(abs(cookie.get_pos()[0] - const.COORDS_NEST[0]), 2) +
                         pow(abs(cookie.get_pos()[1] - const.COORDS_NEST[1]), 2)) < const.CARRING_VELOCITY:
                cookie.set_finished()
                cookie.set_pos(const.COORDS_NEST[0], const.COORDS_NEST[1])
                cookie.set_velocity(0)
                for ant in cookie.get_contributing_ant():
                    ant.set_wandering()
                    ant.clear_approached_cookie()
                    ant.set_angle(random.randint(0, 359))
                    ant.set_velocity(const.ANT_VELOCITY)
                cookie.clear_contributing_ant()
            continue


def draw(win):
    win.fill(const.WHITE)

    for cookie in cookies:
        if cookie.is_sitting():
            cookie.draw_attraction_area(win)

    win.fill(const.LIGHTGREY, (const.WIDTH, 0, const.WIDTH_SIDEBAR, const.HEIGHT))

    for cookie in cookies:
        cookie.draw_cookie(win)

    pygame.draw.rect(win, const.LIGHTBLUE, (const.COORDS_NEST[0] - 5, const.COORDS_NEST[1] - 5, 10, 10))

    for ant in ants:
        ant.draw_ant(win)

    pygame.display.update()


def main(win):
    run = True
    create_ant()
    x = y = z = 0

    while run:

        draw(win)
        update()
        time.sleep(1/steps_per_sec)
        x += 1
        y += 1
        z += 1
        if x == steps_per_sec * new_ant_creation_freq:
            if len(ants) < const.MAX_NUM_ANTS:
                create_ant()
            x = 0

        if y == steps_per_sec * new_cookie_creation_freq:
            if len(cookies) < const.MAX_NUM_COOKIES:
                create_cookie()
            y = 0

        if z == steps_per_sec * 1:
            for ant in ants:
                print(ant)
                #print(ant.trail)
                #print(ant.get_pos()[0], ant.get_pos()[1])
            z = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

main(WIN)
