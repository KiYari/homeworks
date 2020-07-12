WHITE = 1
BLACK = 2


def print_board(board):  # Распечатать доску в текстовом виде
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row + 1, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(chr(col + 65), end='    ')
    print()


def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8


def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def parse_coords(coords):
    new_coords = []
    for cell in coords:
        a = int(ord(cell[0]) - 64)
        b = int(cell[1])
        new_coords.append(b - 1)
        new_coords.append(a - 1)
    print(new_coords)
    return new_coords


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = [[None] * 8 for row in range(8)]

        # White
        for i in range(8):
            self.field[1][i] = Pawn(WHITE)
        self.field[0][0] = Rook(WHITE)
        self.field[0][7] = Rook(WHITE)
        self.field[0][1] = Knight(WHITE)
        self.field[0][6] = Knight(WHITE)
        self.field[0][2] = Bishop(WHITE)
        self.field[0][5] = Bishop(WHITE)
        self.field[0][3] = Queen(WHITE)
        self.field[0][4] = King(WHITE)
        # Black
        for i in range(8):
            self.field[6][i] = Pawn(BLACK)
        self.field[7][0] = Rook(BLACK)
        self.field[7][7] = Rook(BLACK)
        self.field[7][1] = Knight(BLACK)
        self.field[7][6] = Knight(BLACK)
        self.field[7][2] = Bishop(BLACK)
        self.field[7][5] = Bishop(BLACK)
        self.field[7][4] = Queen(BLACK)
        self.field[7][3] = King(BLACK)

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела."""
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]

    def move_piece(self, row, col, row1, col1):
        """ Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False """

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False

        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        else:
            #  Если мы перемещаемся на фигуру
            if self.field[row1][col1].get_color() == self.color:
                return False
            if piece.can_attack(self, row, col, row1, col1):
                piece = self.field[row][col]
                self.field[row][col] = None
                self.field[row1][col1] = piece
                self.color = opponent(self.color)
                return True

        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        self.color = opponent(self.color)  # поменять цвет
        return True

    def is_under_attack(self, row, col, color):

        for r in range(8):
            for c in range(8):
                if not (self.field[r][c] is None):
                    piece = self.field[r][c]
                    if piece.get_color() == color and piece.can_move(self, r, c, row, col):
                        return True
        return False

    def castling0(self):

        row = 0 if self.color == WHITE else 7
        king = self.field[row][4]
        rook = self.field[row][0]
        if not (king is None or rook is None):
            if king.char() == "K" and king.not_moved and rook.char() == "R" and rook.not_moved:
                if rook.can_move(self, row, 0, row, 3):
                    for i in range(1, 5):
                        if self.is_under_attack(row, i, opponent(self.color)):
                            return False
                self.field[row][4] = None
                self.field[row][0] = None
                self.field[row][2] = King(self.color)
                self.field[row][2].moved()
                self.field[row][3] = Rook(self.color)
                self.field[row][3].moved()
                self.color = opponent(self.color)
                return True
        return False

    def castling7(self):

        row = 0 if self.color == WHITE else 7

        king = self.field[row][4]
        rook = self.field[row][7]

        if not (king is None or rook is None):
            if king.char() == "K" and king.not_moved and rook.char() == "R" and rook.not_moved:
                if rook.can_move(self, row, 7, row, 3):
                    for i in range(1, 5):
                        if self.is_under_attack(row, i, opponent(self.color)):
                            return False
                self.field[row][4] = None
                self.field[row][7] = None
                self.field[row][6] = King(self.color)
                self.field[row][6].moved()
                self.field[row][5] = Rook(self.color)
                self.field[row][5].moved()
                self.color = opponent(self.color)
                return True
        return False

    def promotion(self, row, col, row2, col2, char):

        if not (row2 - row == 1 and col2 - col <= 1):
            return False

        if not self.field[row][col].char() == 'P':
            return False

        if char == 'P' or char == 'K':
            return False

        if abs(col2 - col) == 0:
            if self.field[row][col].can_move(self, row, col, row2, col2):
                self.field[row][col] = None
                if char == 'Q':
                    self.field[row2][col2] = Queen(self.color)
                if char == 'N':
                    self.field[row2][col2] = Knight(self.color)
                if char == 'R':
                    self.field[row2][col2] = Rook(self.color)
                if char == 'B':
                    self.field[row2][col2] = Bishop(self.color)
                return False

        if abs(col2 - col) == 1:
            if self.field[row][col].can_attack(self, row, col, row2, col2):
                self.field[row][col] = None
                if char == 'Q':
                    self.field[row2][col2] = Queen(self.color)
                if char == 'N':
                    self.field[row2][col2] = Knight(self.color)
                if char == 'R':
                    self.field[row2][col2] = Rook(self.color)
                if char == 'B':
                    self.field[row2][col2] = Bishop(self.color)
                return True

        return False

    def get_king(self, color):
        for r in range(8):
            for c in range(8):
                if self.field[r][c].char == 'K' and self.color == color:
                    return r, c

    def check_king(self, color):
        steps = []
        kr, kc = self.get_king(self.color)
        for r in range(8):
            for c in range(8):
                if self.field[r][c].get_color() == opponent(self.color):
                    steps.append(self.field[r][c].can_attack(self.field, r, c, kr, kc))
        return steps


class Piece:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.not_moved = True

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(row, c) is None):
                return False
        self.moved()
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def moved(self):
        self.not_moved = False


class Pawn(Piece):
    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if col != col1:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1 and board.field[row1][col1] is None:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        if not board.field[row][col] is not None and board.field[row1][col1].color == opponent(self.color):
            return False
        return True


class Knight(Piece):

    def char(self):
        return "N"

    def can_move(self, board, row, col, row1, col1):

        if abs(row1 - row) + abs(col1 - col) == 3:
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop(Piece):

    def char(self):
        return "B"

    def can_move(self, board, row, col, row1, col1):

        if not (abs(row1 - row) == abs(col1 - col)):
            return False

        step_row = 1 if (row1 > row) else -1
        step_col = 1 if (col1 > col) else -1
        for r, c in zip(range(row + step_row, row1, step_row), range(col + step_col, col1, step_col)):
            if not (board.get_piece(r, c) is None):
                return False

        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen(Piece):

    def char(self):
        return "Q"

    def can_move(self, board, row, col, row1, col1):

        if not ((row1 == row and col1 != col) or (row1 != row and col1 == col) or
                (abs(row1 - row) == abs(col1 - col))):
            return False

        # как ладья
        if row == row1 and col1 != col:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                # Если на пути по горизонтали есть фигура
                if not (board.get_piece(r, col) is None):
                    return False

        if col1 == col and row1 != row:
            step = 1 if (col1 >= col) else -1
            for c in range(col + step, col1, step):
                # Если на пути по вертикали есть фигура
                if not (board.get_piece(row, c) is None):
                    return False

        # как слон
        if abs(row1 - row) == abs(col1 - col) and row != row1 and col1 != col:
            step_row = 1 if (row1 > row) else -1
            step_col = 1 if (col1 > col) else -1
            for r, c in zip(range(row + step_row, row1, step_row), range(col + step_col, col1, step_col)):
                if not (board.get_piece(r, c) is None):
                    return False

        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.not_moved = True

    def char(self):
        return "K"

    def can_move(self, board, row, col, row1, col1):

        if not (abs(row1 - row) <= 1 and abs(col1 - col) <= 1):
            return False

        if not (board.get_piece(row1, col1) is None):
            return False
        self.moved()
        return True

    def moved(self):
        self.not_moved = False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


def main():
    # Создаём доску
    board = Board()
    # Цикл ввода команд игроков
    while True:
        # Выводим доску
        print_board(board)
        # Подсказка по командам
        print('Команды:')
        print('    exit                               -- выход')
        print('    <coord1> <coord2>     -- ход из клетки (coord1) в клетку (coord2)')

        # Выводим чей ход
        if board.current_player_color() == WHITE:
            print('Ход белых: ', end='')
        else:
            print('Ход чёрных: ', end='')

        command = input().split()
        if command == 'exit':
            break

        row, col, row1, col1 = parse_coords(command)

        steps = []
        if any(board.check_king()):
            kr, kc = board.get_king(board.color)
            for r in range(8):
                for c in range(8):
                    steps.append(board.field[kr][kc].can_move(board.field, kr, kc, r, c))
            if any(steps):
                print("Шах")
            else:
                steps = []
                kr, kc = board.get_king((opponent(board.color)))
                for r in range(8):
                    for c in range(8):
                        steps.append(board.field[kr][kc].can_move(board.field, kr, kc, r, c))
                if not any(steps):
                    print('Пат')
                else:
                    print('Мат')

        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')

main()