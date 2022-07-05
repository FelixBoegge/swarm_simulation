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


        if ant.is_approaching():

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


                if ant.get_approached_cookie().is_sitting() and ant.get_approached_cookie().get_occupancy() >= ant.get_approached_cookie().get_size():
                        ant.get_approached_cookie().set_moving()
                        ant.get_approached_cookie().set_velocity(carring_velocity)
                        ant.get_approached_cookie().set_occupancy(cookie.get_size())
                        for ant in ant.get_approached_cookie().get_approaching_ants():
                            ant.set_wandering()
                        for ant in ant.get_approached_cookie().get_waiting_ants():
                            ant.set_carring()
                            ant.get_approached_cookie().add_carring_ant(ant)
                        ant.get_approached_cookie().clear_approaching_ants()
                        ant.get_approached_cookie().clear_waiting_ants()







        if ant.is_waiting():
            if ant.get_approached_cookie().is_moving():
                ant.set_carring()
                ant.set_angle(ant.get_approached_cookie().get_angle_to_nest())




        if ant.is_carring():
            ant.set_angle(ant.get_approached_cookie().get_angle_to_nest())
            ant.set_velocity(carring_velocity)




def update_cookies():
    for cookie in cookies:

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
                cookie.set_pos(coords_nest[0], coords_nest[1])
                for ant in cookie.get_carring_ants():
                    ant.set_wandering()
                    ant.set_angle(random.randint(1, 360))
                    ant.clear_approached_cookie()
                cookie.clear_carring_ants()