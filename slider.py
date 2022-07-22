import pygame
import parameters as para

class Slider:
    X = 885
    WIDTH = 150
    HEIGHT = 2
    POINTER_RADIUS = 7

    def __init__(self, y, min, max, step_size, default):
        self.y = y
        self.slider_bar_space = pygame.Rect(Slider.X, y, Slider.WIDTH, Slider.HEIGHT)
        self.min = min
        self.max = max
        self.step_size = step_size
        self.current = default

    def get_slider_value(self):
        return self.current

    def update_slider(self):
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if Slider.X <= pos[0] <= (Slider.X + Slider.WIDTH) and (self.y - Slider.POINTER_RADIUS) <= pos[1] <= (self.y + Slider.POINTER_RADIUS):
            if click:
                self.current = int((pos[0] - Slider.X) * ((self.max - self.min) / Slider.WIDTH) + self.min)
        return self.current


    def draw_slider(self, win):
        pygame.draw.rect(win, para.GREY, self.slider_bar_space, border_radius=1)
        pygame.draw.circle(win, para.GREEN, (Slider.X + ((self.current / (self.max-self.min)) * Slider.WIDTH), self.y + (Slider.HEIGHT / 2)), Slider.POINTER_RADIUS)

        slider_label_font = pygame.font.SysFont('Areal', 20)
        text_min = slider_label_font.render(str(self.min), True, para.BLACK)
        text_max = slider_label_font.render(str(self.max), True, para.BLACK)
        text_cur = slider_label_font.render(str(self.current), True, para.BLACK)

        win.blit(text_min, (Slider.X - int(text_min.get_width() / 2), self.y - text_min.get_height() - 8))
        win.blit(text_max, (Slider.X + Slider.WIDTH - int(text_max.get_width() / 2), self.y - text_max.get_height() - 8))
        win.blit(text_cur, ((Slider.X + ((self.current / (self.max-self.min))*Slider.WIDTH)) - int(text_cur.get_width() / 2), self.y - text_cur.get_height() - 8))

