import pygame
import random


# Начнем с описания класса поля
class Board:
    # создание поля
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.screen = screen
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.mines = []
        for i in range(10):
            self.mines.append(self.get_cell((random.randint(0, 9) * self.cell_size,
                                             random.randint(0, 9) * self.cell_size)))

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i in range(10):
            self.fill_mines(self.mines[i])

        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(self.screen, pygame.Color('white'),
                                 ((i * self.cell_size, j * self.cell_size), (self.cell_size, self.cell_size)), 1)

    def get_cell(self, pos):
        return pos[0] // self.cell_size, pos[1] // self.cell_size

    def fill_mines(self, pos):
        pygame.draw.rect(self.screen, pygame.Color('red'),
                         ((pos[0] * self.cell_size, pos[1] * self.cell_size),
                          (self.cell_size, self.cell_size)))

    def get_click(self, pos):
        cell = self.get_cell(pos)
        count = 0
        if cell not in self.mines:
            if (cell[0] - 1, cell[1] - 1) in self.mines:
                count += 1
            if (cell[0], cell[1] - 1) in self.mines:
                count += 1
            if (cell[0] + 1, cell[1] - 1) in self.mines:
                count += 1
            if (cell[0] + 1, cell[1]) in self.mines:
                count += 1
            if (cell[0] + 1, cell[1] + 1) in self.mines:
                count += 1
            if (cell[0], cell[1] + 1) in self.mines:
                count += 1
            if (cell[0] - 1, cell[1] + 1) in self.mines:
                count += 1
            if (cell[0] - 1, cell[1]) in self.mines:
                count += 1

            score = pygame.font.SysFont('serif', 20)
            text = score.render(str(count), 1, pygame.Color('white'))
            self.screen.blit(text, (cell[0] * self.cell_size + 10, cell[1] * self.cell_size + 5))


size = width, height = (300, 300)
screen = pygame.display.set_mode(size)
pygame.init()

board = Board(10, 10, screen)
running = True
screen.fill((0, 0, 0))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    board.render()
    pygame.display.flip()
