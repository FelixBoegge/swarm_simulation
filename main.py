import pygame


pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGREY = (200, 200,200)

WIDTH = 800
HEIGHT = 600
WIDTH_SIDEBAR = 200


WIN = pygame.display.set_mode((WIDTH+WIDTH_SIDEBAR, HEIGHT))
pygame.display.set_caption('swarm simulation')


def draw(win):
    win.fill(WHITE)
    win.fill(LIGHTGREY, (WIDTH, 0, WIDTH_SIDEBAR, HEIGHT))

    pygame.display.update()


def main(win):
    run = True

    while run:
        draw(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


    pygame.quit()


main(WIN)
