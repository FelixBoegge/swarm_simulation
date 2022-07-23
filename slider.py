import pygame
import parameters as para

class Slider:
    X_TEXT = 810
    WIDTH_TEXT = 870

    X_SLIDER = 935
    WIDTH_SLIDER = 150
    HEIGHT_SLIDER = 2
    POINTER_RADIUS = 7

    def __init__(self, y, min, max, step_size, default, label_text):
        self.y = y
        self.slider_bar_space = pygame.Rect(Slider.X_SLIDER, y, Slider.WIDTH_SLIDER, Slider.HEIGHT_SLIDER)
        self.min = min
        self.max = max
        self.step_size = step_size
        self.current = default
        self.label_text = label_text

    def get_slider_value(self):
        return self.current

    def update_slider(self):
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if Slider.X_SLIDER <= pos[0] <= (Slider.X_SLIDER + Slider.WIDTH_SLIDER) and (self.y - Slider.POINTER_RADIUS*2) <= pos[1] <= (self.y + Slider.POINTER_RADIUS*2):
            if click[0]:
                self.current = int(((pos[0] - Slider.X_SLIDER) * ((self.max - self.min) / Slider.WIDTH_SLIDER))) + self.min
        return self.current


    def draw_slider(self, win):
        pygame.draw.rect(win, para.GREY, self.slider_bar_space, border_radius=1)
        pygame.draw.circle(win, para.GREEN, (Slider.X_SLIDER + ((self.current / (self.max - self.min)) * Slider.WIDTH_SLIDER), self.y + (Slider.HEIGHT_SLIDER / 2)), Slider.POINTER_RADIUS)

        slider_label_font = pygame.font.SysFont('Areal', 20)
        text_min = slider_label_font.render(str(self.min), True, para.GREY)
        text_max = slider_label_font.render(str(self.max), True, para.GREY)
        text_cur = slider_label_font.render(str(self.current), True, para.BLACK)

        win.blit(text_min, (Slider.X_SLIDER - int(text_min.get_width() / 2), self.y + 4))
        win.blit(text_max, (Slider.X_SLIDER + Slider.WIDTH_SLIDER - int(text_max.get_width() / 2), self.y + 4))
        win.blit(text_cur, ((Slider.X_SLIDER + ((self.current / (self.max - self.min)) * Slider.WIDTH_SLIDER)) - int(text_cur.get_width() / 2), self.y - text_cur.get_height() - 8))

        slider_text_font = pygame.font.SysFont('Times New Roman', 15)
        text = slider_text_font.render(self.label_text, True, para.BLACK)

        win.blit(text, (Slider.X_TEXT, self.y - int(text.get_height()/2)))

