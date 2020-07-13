import pygame as pg

w, n = [int(i) for i in input().split()]
while w % n != 0:
    w, n = [int(i) for i in input().split()]

pg.init()

size = width, height = w, w

screen = pg.display.set_mode(size)


def draw():
    for i in range(n):
        for j in range(n):
            cell_size = w // n
            if (i + j + 1) % 2 == 0:
                pg.draw.rect(screen, pg.Color("black"),
                             [cell_size * i, cell_size * j, cell_size * i + cell_size, cell_size * j + cell_size])
            else:
                pg.draw.rect(screen, pg.Color("white"),
                             [cell_size * i, cell_size * j, cell_size * i + cell_size, cell_size * j + cell_size])


draw()

while pg.event.wait().type != pg.QUIT:
    pg.display.flip()

pg.quit()
