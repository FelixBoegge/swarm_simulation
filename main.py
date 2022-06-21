import pygame


pygame.init()

WHITE = (255, 255, 255)

WIDTH = 800
HEIGHT = 600


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('swarm simulation')


def draw(win):
    win.fill(WHITE)


def main(win):
    run = True

    while run:
        draw(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


    pygame.quit()

main(WIN)