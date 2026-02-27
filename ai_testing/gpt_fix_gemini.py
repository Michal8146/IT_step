import pygame
import random
import os

# Inicializace Pygame
pygame.init()

# Rozměry mřížky
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30

# Rozměry okna
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700

# Barvy
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (128, 0, 128),  # T
    (255, 0, 0)     # Z
]

# Tvary Tetromin
SHAPES = [
    [['.....',
      '.....',
      '..O..',
      '..O..',
      '..O..',
      '..O..',
      '.....'],],  # I

    [['.....',
      '.....',
      '..O..',
      '..O..',
      '..OO.',
      '.....'],],  # J

    [['.....',
      '.....',
      '..O..',
      '..O..',
      '.OO..',
      '.....'],],  # L

    [['.....',
      '.....',
      '..OO.',
      '..OO.',
      '.....'],],  # O

    [['.....',
      '.....',
      '..OO.',
      '.OO..',
      '.....'],],  # S

    [['.....',
      '.....',
      '..O..',
      '.OOO.',
      '.....'],],  # T

    [['.....',
      '.....',
      '.OO..',
      '..OO.',
      '.....'],],  # Z
]

# Rozšíření tvarů o rotace
def rotate(shape):
    return [''.join(row[::-1]) for row in zip(*shape)]

for shape in SHAPES:
    base = shape[0]
    for _ in range(3):
        base = rotate(base)
        shape.append(base)

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.rotation = 0
        self.color = COLORS[SHAPES.index(shape)]

def create_grid(locked_positions):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for (x, y), color in locked_positions.items():
        if y >= 0:
            grid[y][x] = color
    return grid

def convert_shape_format(piece):
    positions = []
    shape = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape):
        for j, column in enumerate(line):
            if column == 'O':
                positions.append((piece.x + j, piece.y + i))
    return positions

def valid_space(piece, grid):
    accepted = [[(j, i) for j in range(GRID_WIDTH) if grid[i][j] == BLACK] for i in range(GRID_HEIGHT)]
    accepted = [j for sub in accepted for j in sub]
    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted:
            if pos[1] >= 0:
                return False
    return True

def check_lost(positions):
    for _, y in positions:
        if y < 1:
            return True
    return False

def get_new_piece():
    return Piece(3, 0, random.choice(SHAPES))

def draw_grid(surface, grid):
    for i in range(GRID_HEIGHT):
        pygame.draw.line(surface, GRAY, (0, i * BLOCK_SIZE), (GRID_WIDTH * BLOCK_SIZE, i * BLOCK_SIZE))
        for j in range(GRID_WIDTH):
            pygame.draw.line(surface, GRAY, (j * BLOCK_SIZE, 0), (j * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))

def draw_window(surface, grid, score, high_score):
    surface.fill(BLACK)
    font = pygame.font.SysFont("comicsans", 36)
    label = font.render(f"Score: {score}", 1, WHITE)
    surface.blit(label, (WINDOW_WIDTH - 200, 30))

    label = font.render(f"High Score: {high_score}", 1, WHITE)
    surface.blit(label, (WINDOW_WIDTH - 200, 80))

    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            pygame.draw.rect(surface, grid[i][j], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    draw_grid(surface, grid)
    pygame.draw.rect(surface, WHITE, (0, 0, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE), 4)
    pygame.display.update()

def clear_rows(grid, locked):
    cleared = 0
    for i in range(len(grid)-1, -1, -1):
        if BLACK not in grid[i]:
            cleared += 1
            for j in range(GRID_WIDTH):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if cleared > 0:
        # posuň řádky dolů
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < i:
                new_key = (x, y + cleared)
                locked[new_key] = locked.pop(key)

    return cleared

def load_high_score():
    try:
        with open("high_score.txt", "r") as f:
            val = f.read()
            return int(val.strip()) if val.strip().isdigit() else 0
    except:
        return 0

def save_high_score(score):
    with open("high_score.txt", "w") as f:
        f.write(str(score))

def main():
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_new_piece()
    next_piece = get_new_piece()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    score = 0
    high_score = load_high_score()

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick(60)

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                save_high_score(high_score)
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)

        shape_pos = convert_shape_format(current_piece)

        for x, y in shape_pos:
            if y >= 0:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                locked_positions[(pos[0], pos[1])] = current_piece.color
            current_piece = next_piece
            next_piece = get_new_piece()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10
            high_score = max(high_score, score)

        draw_window(win, grid, score, high_score)

        if check_lost(locked_positions):
            run = False

    save_high_score(high_score)

if __name__ == "__main__":
    main()
