import pygame
import random

# Init
pygame.init()

# Constants
BLOCK_SIZE = 40
COLUMNS = 10
ROWS = 20
SCREEN_WIDTH = COLUMNS * BLOCK_SIZE
SCREEN_HEIGHT = ROWS * BLOCK_SIZE
FPS = 60

# Colors
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (128, 0, 128),  # T
    (255, 0, 0)     # Z
]

SHAPES = [
    [[1, 1, 1, 1]],                      # I
    [[1, 0, 0], [1, 1, 1]],              # J
    [[0, 0, 1], [1, 1, 1]],              # L
    [[1, 1], [1, 1]],                    # O
    [[0, 1, 1], [1, 1, 0]],              # S
    [[0, 1, 0], [1, 1, 1]],              # T
    [[1, 1, 0], [0, 1, 1]]               # Z
]

# Init display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Game board
board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = COLORS[SHAPES.index(self.shape)]
        self.x = COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        original_shape = self.shape
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        if self.collision():
            self.shape = original_shape

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        if self.collision():
            self.x -= dx
            self.y -= dy
            return False
        return True

    def collision(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    nx = self.x + x
                    ny = self.y + y
                    if nx < 0 or nx >= COLUMNS or ny >= ROWS:
                        return True
                    if ny >= 0 and board[ny][nx]:
                        return True
        return False

    def freeze(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell and self.y + y >= 0:
                    board[self.y + y][self.x + x] = self.color

def clear_lines():
    global board, score
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    cleared = ROWS - len(new_board)
    score += cleared * 100
    for _ in range(cleared):
        new_board.insert(0, [0 for _ in range(COLUMNS)])
    board = new_board

def draw_grid():
    for y in range(ROWS):
        for x in range(COLUMNS):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

def draw_board():
    for y in range(ROWS):
        for x in range(COLUMNS):
            color = board[y][x]
            if color:
                pygame.draw.rect(screen, color, (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), border_radius=6)
                pygame.draw.rect(screen, BLACK, (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 2)

def draw_piece(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, piece.color, rect, border_radius=6)
                pygame.draw.rect(screen, BLACK, rect, 2)

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over():
    return any(board[0][x] for x in range(COLUMNS))

# Main loop
def main():
    global score
    score = 0
    current = Tetromino()
    fall_time = 0
    fall_speed = 0.5
    running = True

    while running:
        dt = clock.tick(FPS) / 1000
        fall_time += dt

        if fall_time >= fall_speed:
            if not current.move(0, 1):
                current.freeze()
                clear_lines()
                if game_over():
                    print("Game Over")
                    running = False
                current = Tetromino()
            fall_time = 0

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    current.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    current.move(0, 1)
                elif event.key == pygame.K_UP:
                    current.rotate()

        # Draw
        screen.fill(BLACK)
        draw_board()
        draw_piece(current)
        draw_grid()
        draw_score()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
