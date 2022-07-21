import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
import random
import math

import parameters as para
from ants import Ant
from cookie import Cookie

pygame.init()


ants = []
cookies = []

WIN = pygame.display.set_mode((para.WIDTH + para.WIDTH_SIDEBAR, para.HEIGHT))
pygame.display.set_caption('swarm simulation')


def create_cookie():
    cookies.append(Cookie())


def create_ant():
    ants.append(Ant())


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
    collected_cookies = 0
    cookie_score = 0
    killed_ants = 0

    for ant in ants:
        if ant.get_step_counter() >= 50:
            r = random.randint(1,10)
            if r > 5:
                ant.change_random_angle()
            ant.set_step_counter(0)
        if not ant.is_following():
            ant.set_new_pos()


        if ant.is_wandering():
            ant.inc_step_counter()
            ant.set_velocity(para.ANT_VELOCITY)
            for cookie in cookies:
                if get_distance(ant, cookie) < cookie.get_attraction() and cookie.is_sitting():
                    ant.set_approaching()
                    ant.set_approached_cookie(cookie)
                    ant.set_angle(get_angle(ant, cookie))
                    cookie.add_approaching_ant(ant)

            for a in ants:
                if a != ant and (a.is_wandering() or a.is_following()):
                    for i, scent in enumerate(a.get_trail()):
                        if scent != None and ant.get_step_counter() > 20:
                            dx = abs(ant.get_pos()[0] - scent[0])
                            dy = abs(ant.get_pos()[1] - scent[1])
                            d = math.sqrt(pow(dx, 2) + pow(dy, 2))
                            if d < para.ANT_VELOCITY:
                                r = random.randint(0, para.LENGTH_TRAIL)
                                if r >= (para.LENGTH_TRAIL - i):
                                    ant.set_following()
                                    ant.set_followed_ant(a, i)
                                    a.add_following_ant(ant)
                                    killed_ants = check_death_cycle(ant)
                        continue


        if ant.is_following():
            ant.set_pos(ant.get_followed_ant().get_trail()[ant.get_followed_ant_trail()][0], ant.get_followed_ant().get_trail()[ant.get_followed_ant_trail()][1])
            if ant.get_followed_ant().is_approaching():
                ant.set_approaching()
                ant.set_approached_cookie(ant.get_followed_ant().get_approached_cookie())
                ant.set_angle(get_angle(ant, ant.get_followed_ant().get_approached_cookie()))
                ant.get_followed_ant().get_approached_cookie().add_approaching_ant(ant)


        if ant.is_approaching():
            ant.set_step_counter(0)
            if get_distance(ant, ant.get_approached_cookie()) < ant.get_approached_cookie().get_size():
                ant.set_waiting()
                ant.get_approached_cookie().remove_approaching_ant(ant)
                ant.get_approached_cookie().add_contributing_ant(ant)
                ant.set_velocity(0)
                x = ant.get_approached_cookie().get_pos()[0] - math.cos(math.radians(ant.angle)) * ant.get_approached_cookie().get_size()
                y = ant.get_approached_cookie().get_pos()[1] + math.sin(math.radians(ant.angle)) * ant.get_approached_cookie().get_size()
                ant.set_pos(x, y)

                ant.get_approached_cookie().inc_attraction()
                ant.get_approached_cookie().inc_occupancy()


        if ant.is_waiting():
            if ant.get_approached_cookie().is_moving():
                ant.set_carring()
                ant.set_angle(ant.get_approached_cookie().get_angle_to_nest())
                ant.set_velocity(para.CARRING_VELOCITY)


    for cookie in cookies:
        cookie.set_new_pos()

        if cookie.is_sitting():
            if cookie.get_occupancy() >= cookie.get_size():
                cookie.set_moving()
                cookie.set_velocity(para.CARRING_VELOCITY)
                cookie.set_occupancy(cookie.get_size())
                for ant in cookie.get_approaching_ant():
                    ant.clear_approached_cookie()
                    ant.set_wandering()
                cookie.clear_approaching_ant()
                for ant in cookie.get_contributing_ant():
                    ant.set_carring()
                    ant.set_velocity(para.CARRING_VELOCITY)
                    ant.set_angle(cookie.get_angle_to_nest())

        if cookie.is_moving():
            if math.sqrt(pow(abs(cookie.get_pos()[0] - para.COORDS_NEST[0]), 2) +
                         pow(abs(cookie.get_pos()[1] - para.COORDS_NEST[1]), 2)) < para.CARRING_VELOCITY:
                cookie.set_finished()
                collected_cookies += 1
                cookie_score += cookie.get_size()
                for ant in cookie.get_contributing_ant():
                    ant.set_wandering()
                    ant.set_angle(random.randint(0, 359))
                    ant.set_velocity(para.ANT_VELOCITY)
                    ant.clear_approached_cookie()
                    ant.clear_trail()
                cookie.clear_contributing_ant()
                cookies.remove(cookie)

    return collected_cookies, cookie_score, killed_ants


def check_death_cycle(ant):
    death_cycle = []
    next_ant = ant
    while next_ant.is_following():
        next_ant = next_ant.get_followed_ant()
        death_cycle.append(next_ant)
        if next_ant == ant:
            for ant in death_cycle:
                for a in ant.get_following_ants():
                    a.clear_followed_ant()
                    a.set_wandering()
                ants.remove(ant)
            return len(death_cycle)
    return 0


def draw(win):
    #win.fill(para.WHITE)
    win.blit(para.BACKGROUND, (0, 0))

    for cookie in cookies:
        if cookie.is_sitting():
            cookie.draw_attraction_area(win)

    win.fill(para.LIGHTGREY, (para.WIDTH, 0, para.WIDTH_SIDEBAR, para.HEIGHT))
    #slider = Slider(win, 820, 20, 160, 30) #pygame_widgets.widget.Slider(title='max num ants', default_value=50, range_values=(1, 100), range_width=150, increment=1)
    #win.blit(win, slider)

    pygame.draw.rect(win, para.DARKGREY, (para.COORDS_NEST[0] - 5, para.COORDS_NEST[1] - 5, 10, 10))

    for cookie in cookies:
        cookie.draw_cookie(win)

    for ant in ants:
        ant.draw_ant_trail(win)

    for ant in ants:
        ant.draw_ant(win)

    pygame.display.update()


def main(win):
    run = True
    collected_cookies = cookie_score = killed_ants = 0
    ant_creation_helper = cookie_creation_helper = 0

    for _ in range(para.NUM_START_ANTS):
        create_ant()
    for _ in range(para.NUM_START_COOKIES):
        create_cookie()

    while run:

        draw(win)
        cookie_add, score_add, killed_ants_add = update()
        collected_cookies += cookie_add
        cookie_score += score_add
        killed_ants += killed_ants_add
        pygame.time.delay(1000//para.STEPS_PER_SECOND)
        ant_creation_helper += 1
        cookie_creation_helper += 1

        if ant_creation_helper >= para.STEPS_PER_SECOND * para.NEW_ANT_CREATION_FREQUENCY:
            if len(ants) < para.MAX_NUM_ANTS:
                create_ant()
            ant_creation_helper = 0

        if cookie_creation_helper >= para.STEPS_PER_SECOND * para.NEW_COOKIE_CREATION_FREQUENCY:
            if len(cookies) < para.MAX_NUM_COOKIES:
                create_cookie()
            cookie_creation_helper = 0


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

main(WIN)
