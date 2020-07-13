import pygame
import math

size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.init()

ORANGE = pygame.Color('orange')
running = True
draw = True
mult = 2

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if draw:
                    draw = False
                else:
                    draw = True

    color = pygame.Color('white')
    hsv = color.hsva
    color.hsva = (hsv[0] + mult * 3, hsv[1] + mult * 3, hsv[2], hsv[3])
    pygame.draw.circle(screen, color, (250, 250), 200, 1)
    if draw:
        for i in range(360):
            x = int(math.cos(math.radians(i)) * 200) + height // 2
            y = int(math.sin(math.radians(i)) * 200) + height // 2
            x2 = int(math.cos(math.radians(mult * i)) * 200) + height // 2
            y2 = int(math.sin(math.radians(mult * i)) * 200) + height // 2
            pygame.draw.aaline(screen, color, [x, y], [x2, y2])
        mult += 0.01
        pygame.display.flip()
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, color, (250, 250), 200, 1)
