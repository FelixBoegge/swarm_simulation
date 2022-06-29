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
steps_per_sec = 25
num_ants = 50
num_cookies = 2
min_size_cookie = 5
max_size_cookie = 10
ant_velocity = 3
carring_velocity = 1
ants = []
cookies = []
#distances = {}
#distances = [0 for x in range(num_cookies)]


WIN = pygame.display.set_mode((const.WIDTH+const.WIDTH_SIDEBAR, const.HEIGHT))
pygame.display.set_caption('swarm simulation')



for _ in range(num_ants):
    #x = random.randint(0, const.WIDTH)
    #y = random.randint(0, const.HEIGHT)
    x = coords_nest[0]
    y = coords_nest[1]
    angle = random.randint(0, 359)
    velocity = ant_velocity
    ants.append(Ant(x, y, angle, velocity))

for _ in range(num_cookies):
    x = random.randint(20, const.WIDTH - 20)
    y = random.randint(20, const.HEIGHT - 20)
    size = random.randint(min_size_cookie, max_size_cookie)
    cookies.append(Cookie(x, y, size))

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


#def get_distances(cookies, ants):
 #   for ant in ants:
  #      if ant.is_wandering() or ant.is_approaching():
   #         distances = {}
    #        for cookie in cookies:
     #           distances[cookie] = (get_distance(ant, cookie))
      #      ant.set_ant_cookies_distances(distances)


def update_ants():
    for ant in ants:
        ant.set_new_pos()

        if ant.is_wandering():
            ant.set_velocity(ant_velocity)

            for cookie in cookies:
                if get_distance(ant, cookie) <= cookie.get_attraction() and cookie.is_sitting():
                    ant.set_approaching()
                    ant.set_approached_cookie(cookie)
                    cookie.add_approaching_ant(ant)
                    ant.set_angle(get_angle(ant, cookie))
                continue



        elif ant.is_approaching():

            if get_distance(ant, ant.get_approached_cookie()) <= ant.get_approached_cookie().get_radius():
                ant.set_waiting()
                ant.set_velocity(0)

                x = ant.get_approached_cookie().get_pos()[0] - math.cos(math.radians(ant.angle)) * ant.get_approached_cookie().get_radius()
                y = ant.get_approached_cookie().get_pos()[1] + math.sin(math.radians(ant.angle)) * ant.get_approached_cookie().get_radius()
                ant.set_pos(x, y)

                ant.get_approached_cookie().remove_approaching_ant(ant)
                ant.get_approached_cookie().add_waiting_ant(ant)
                ant.get_approached_cookie().inc_occupancy()
                ant.get_approached_cookie().inc_attraction()


        #elif ant.is_waiting():
         #   if ant.get_approached_cookie().is_moving():
          #      ant.set_carring()
           #     ant.set_angle(ant.get_approached_cookie().get_angle_to_nest())


        elif ant.is_carring():
            ant.set_angle(ant.get_approached_cookie().get_angle_to_nest())
            ant.set_velocity(carring_velocity)


def update_cookies():
    for cookie in cookies:
      #  for ant in ants:
           # if get_distance(ant, cookie) <= cookie.attraction and cookie.is_sitting():
            #    cookie.add_approaching_ant(ant)

       # for ant in cookie.get_approaching_ants():
        #    if get_distance(ant, cookie) <= cookie.get_radius():
         #       ant.set_waiting()
          #      cookie.remove_approaching_ant(ant)
           #     cookie.add_waiting_ant(ant)




        if cookie.is_sitting():
          if cookie.get_occupancy() >= cookie.get_size():
                cookie.set_moving()
                cookie.set_velocity(carring_velocity)
                cookie.set_occupancy(cookie.get_size())
                for ant in cookie.get_approaching_ants():
                    ant.set_wandering()
                for ant in cookie.get_waiting_ants():
                    ant.set_carring()
                    cookie.add_carring_ant(ant)
                cookie.clear_approaching_ants()
                cookie.clear_waiting_ants()

        elif cookie.is_moving():
            cookie.set_new_pos()
            if math.sqrt(pow(abs(cookie.get_pos()[0] - coords_nest[0]),2) + pow(abs(cookie.get_pos()[1] - coords_nest[1]),2)) < cookie.get_velocity():
                cookie.set_finished()
                #x = coords_nest[0] - math.cos(math.radians(cookie.angle_to_nest)) * nest_radius
                #y = coords_nest[1] + math.sin(math.radians(cookie.angle_to_nest)) * nest_radius
                cookie.set_pos(coords_nest[0], coords_nest[1])
                for ant in cookie.get_carring_ants():
                    ant.set_wandering()
                    ant.set_angle(random.randint(1, 360))
                    ant.clear_approached_cookie()
                    #ant.clear_approached_cookie_id()
                cookie.clear_carring_ants()











def draw(win):
    win.fill(const.WHITE)

    for cookie in cookies:
        if cookie.is_sitting():
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
#        get_distances(cookies, ants)
        update_ants()
        update_cookies()
        time.sleep(1/steps_per_sec)

        for i, cookie in enumerate(cookies):
            print(f"{i} Approaching: {len(cookie.get_carring_ants())}")
            print(f"{i} Waiting: {len(cookie.get_waiting_ants())}")
            print(f"{i} Carring: {len(cookie.get_carring_ants())}")



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


    pygame.quit()


main(WIN)
