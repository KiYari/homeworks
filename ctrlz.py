import pygame

size = width, height = 500, 500
screen = pygame.display.set_mode(size)
screen2 = pygame.Surface(screen.get_size())
x1, y1, w, h = 0, 0, 0, 0

running = True
drawing = False
rects = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            x1, y1 = event.pos
            w, h = 0, 0

        if event.type == pygame.MOUSEBUTTONUP:
            screen2.blit(screen, (0, 0))
            drawing = False
            rects.append((x1, y1, w, h))
        if event.type == pygame.MOUSEMOTION:
            w, h = event.pos[0] - x1, event.pos[1] - y1

        if event.type == pygame.KEYDOWN and event.key == pygame.K_z \
                and event.mod == pygame.KMOD_LCTRL:
            if len(rects) != 0:
                rects.pop()
                screen2.fill((0, 0, 0, 0))
                for coords in rects:
                    pygame.draw.rect(screen2, pygame.Color('white'), coords, 1)
                screen.blit(screen2, (0, 0))
        if drawing:
            screen.blit(screen2, (0, 0))
            pygame.draw.rect(screen, pygame.Color('white'), (x1, y1, w, h), 1)     
    pygame.display.flip()
