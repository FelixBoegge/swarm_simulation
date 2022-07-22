import pygame
#import pygame_widgets
#from pygame_widgets.slider import Slider
import random
import math

import parameters as para
from ants import Ant
from cookie import Cookie
from slider import Slider

pygame.init()


ants = []
cookies = []
sliders = {}
slider_values = {}

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
            ant.set_velocity(slider_values['velocity'])
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
                            if d < slider_values['velocity']:
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
                    ant.set_velocity(slider_values['velocity'])
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


def create_sliders():
    sliders = {}
    sliders['max_ants'] = Slider(50, min=1, max=para.MAX_NUM_ANTS, step_size=1, default=30, label_text='max num ants')
    sliders['max_cookies'] = Slider(100, min=1, max=para.MAX_NUM_COOKIES, step_size=1, default=5, label_text='max num Cookies')
    sliders['ant_creation_freq'] = Slider(150, min=1, max=5, step_size=1, default=2, label_text='new ant cycle')
    sliders['cookie_creation_freq'] = Slider(200, min=1, max=10, step_size=1, default=5, label_text='new cookie cycle')
    sliders['velocity'] = Slider(250, min=1, max=10, step_size=1, default=para.ANT_VELOCITY, label_text='velocity')
    return sliders


def draw(win, sliders, collected_cookies, cookie_score, killed_ants, time_counter):
    win.blit(para.BACKGROUND, (0, 0))

    for cookie in cookies:
        if cookie.is_sitting():
            cookie.draw_attraction_area(win)

    win.fill(para.LIGHTGREY, (para.WIDTH, 0, para.WIDTH_SIDEBAR, para.HEIGHT))

    pygame.draw.rect(win, para.DARKGREY, (para.COORDS_NEST[0] - 5, para.COORDS_NEST[1] - 5, 10, 10))

    for cookie in cookies:
        cookie.draw_cookie(win)

    for ant in ants:
        ant.draw_ant_trail(win)

    for ant in ants:
        ant.draw_ant(win)

    for slider in sliders:
        sliders[slider].draw_slider(win)

    info_font = pygame.font.SysFont('Times New Roman', 15)

    cur_ants_text = info_font.render('current number of ants', True, para.BLACK)
    cur_cookies_text = info_font.render('current number of cookies', True, para.BLACK)
    cur_food_text = info_font.render('current food available', True, para.BLACK)
    collected_cookies_text = info_font.render('collected cookies', True, para.BLACK)
    collected_food_text = info_font.render('amount of food colleced', True, para.BLACK)
    killed_ants_text = info_font.render('ants killed in death cycles', True, para.BLACK)
    time_text = info_font.render('time passed [seconds]', True, para.BLACK)

    cur_ants_val_text = info_font.render(str(len(ants)), True, para.BLACK)
    cur_cookies_val_text = info_font.render(str(len(cookies)), True, para.BLACK)
    cur_food_val_text = info_font.render(str(sum(cookie.get_size() for cookie in cookies)), True, para.BLACK)
    collected_cookies_val_text = info_font.render(str(collected_cookies), True, para.GREEN)
    collected_food_val_text = info_font.render(str(cookie_score), True, para.GREEN)
    killed_ants_val_text = info_font.render(str(killed_ants), True, para.RED)
    time_val_text = info_font.render(str(time_counter), True, para.BLACK)

    win.blit(cur_ants_text, (Slider.X_TEXT, 350))
    win.blit(cur_ants_val_text, (1030, 350))

    win.blit(cur_cookies_text, (Slider.X_TEXT, 380))
    win.blit(cur_cookies_val_text, (1030, 380))

    win.blit(cur_food_text, (Slider.X_TEXT, 410))
    win.blit(cur_food_val_text, (1030, 410))

    win.blit(collected_cookies_text, (Slider.X_TEXT, 440))
    win.blit(collected_cookies_val_text, (1030, 440))

    win.blit(collected_food_text, (Slider.X_TEXT, 470))
    win.blit(collected_food_val_text, (1030, 470))

    win.blit(killed_ants_text, (Slider.X_TEXT, 500))
    win.blit(killed_ants_val_text, (1030, 500))

    win.blit(time_text, (Slider.X_TEXT, 530))
    win.blit(time_val_text, (1030, 530))

    pygame.display.update()


def main(win):
    run = True
    collected_cookies = cookie_score = killed_ants = time_counter = 0
    ant_creation_helper = cookie_creation_helper = time_counter_helper = 0

    for _ in range(para.NUM_START_ANTS):
        create_ant()
    for _ in range(para.NUM_START_COOKIES):
        create_cookie()

    sliders = create_sliders()

    while run:

        for slider in sliders:
            slider_values[slider] = sliders[slider].update_slider()

        draw(win, sliders, collected_cookies, cookie_score, killed_ants, time_counter)
        cookie_add, score_add, killed_ants_add = update()
        collected_cookies += cookie_add
        cookie_score += score_add
        killed_ants += killed_ants_add
        pygame.time.delay(1000//para.STEPS_PER_SECOND)
        ant_creation_helper += 1
        cookie_creation_helper += 1
        time_counter_helper += 1

        if ant_creation_helper >= para.STEPS_PER_SECOND * slider_values['ant_creation_freq']:
            if len(ants) < slider_values['max_ants']:
                create_ant()
            ant_creation_helper = 0

        if cookie_creation_helper >= para.STEPS_PER_SECOND * slider_values['cookie_creation_freq']:
            if len(cookies) < slider_values['max_cookies']:
                create_cookie()
            cookie_creation_helper = 0

        if time_counter_helper >= para.STEPS_PER_SECOND:
            time_counter += 1
            time_counter_helper = 0


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

main(WIN)
