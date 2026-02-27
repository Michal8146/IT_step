import pygame
import random

# Game constants
CELL_SIZE = 30
COLS, ROWS = 10, 20
WIDTH, HEIGHT = CELL_SIZE * COLS, CELL_SIZE * ROWS
FPS = 60

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],            # I
    [[1, 1], [1, 1]],          # O
    [[0, 1, 0], [1, 1, 1]],    # T
    [[1, 0, 0], [1, 1, 1]],    # J
    [[0, 0, 1], [1, 1, 1]],    # L
    [[1, 1, 0], [0, 1, 1]],    # S
    [[0, 1, 1], [1, 1, 0]]     # Z
]
COLORS = [
    (0, 255, 255), (255, 255, 0), (128, 0, 128),
    (0, 0, 255), (255, 165, 0), (0, 255, 0), (255, 0, 0)
]

# Tetromino class
class Tetromino:
    def __init__(self, x, y, shape, color):
        self.x, self.y = x, y
        self.shape = shape
        self.color = color

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Game functions
def create_board():
    return [[(0, 0, 0) for _ in range(COLS)] for _ in range(ROWS)]

def valid_move(board, tetro, dx=0, dy=0, rot=False):
    shape = tetro.shape
    if rot:
        shape = [list(row) for row in zip(*shape[::-1])]
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                nx, ny = tetro.x + x + dx, tetro.y + y + dy
                if nx < 0 or nx >= COLS or ny >= ROWS or (ny >= 0 and board[ny][nx] != (0, 0, 0)):
                    return False
    return True

def merge(board, tetro):
    for y, row in enumerate(tetro.shape):
        for x, cell in enumerate(row):
            if cell:
                board[tetro.y + y][tetro.x + x] = tetro.color

def clear_lines(board):
    lines = [row for row in board if any(cell == (0, 0, 0) for cell in row)]
    cleared = ROWS - len(lines)
    return [[(0, 0, 0)] * COLS for _ in range(cleared)] + lines, cleared

def new_tetromino():
    idx = random.randint(0, len(SHAPES) - 1)
    return Tetromino(COLS // 2 - 2, 0, [row[:] for row in SHAPES[idx]], COLORS[idx])

# Main game
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    board = create_board()
    tetro = new_tetromino()
    fall_time, fall_speed = 0, 0.5
    running, game_over = True, False

    while running:
        dt = clock.tick(FPS) / 1000
        fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and valid_move(board, tetro, dx=-1):
                    tetro.x -= 1
                if event.key == pygame.K_RIGHT and valid_move(board, tetro, dx=1):
                    tetro.x += 1
                if event.key == pygame.K_DOWN and valid_move(board, tetro, dy=1):
                    tetro.y += 1
                if event.key == pygame.K_UP and valid_move(board, tetro, rot=True):
                    tetro.rotate()

        if not game_over and fall_time > fall_speed:
            if valid_move(board, tetro, dy=1):
                tetro.y += 1
            else:
                merge(board, tetro)
                board, _ = clear_lines(board)
                tetro = new_tetromino()
                if not valid_move(board, tetro):
                    game_over = True
            fall_time = 0

        # Draw
        screen.fill((0, 0, 0))
        for y in range(ROWS):
            for x in range(COLS):
                color = board[y][x]
                if color != (0, 0, 0):
                    pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for y, row in enumerate(tetro.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, tetro.color, ((tetro.x + x) * CELL_SIZE, (tetro.y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
