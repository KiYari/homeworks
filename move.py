import pygame

size = width, height = (300, 300)
screen = pygame.display.set_mode(size)
pygame.init()

screen.fill((0, 0, 0))
x1, y1 = 0, 0
pygame.draw.rect(screen, pygame.Color('white'), [x1, y1, 100, 100])

x_click = 0
y_click = 0
x2 = 0
y2 = 0

running = True
drawing = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            screen.fill((0, 0, 0))
            if x1 <= event.pos[0] <= x1 + 100 and y1 <= event.pos[1] <= y1 + 100:
                x_click = event.pos[0]
                y_click = event.pos[1]
                x2 = x1
                y2 = y1
                drawing = True
            else:
                pygame.draw.rect(screen, pygame.Color('white'), [x1, y1, 100, 100])
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        if drawing:
            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, pygame.Color('white'), [x1, y1, 100, 100])
            x1 = x2 + event.pos[0] - x_click
            y1 = y2 + event.pos[1] - y_click
        pygame.display.flip()