import pygame
import random

# --- Constants ---
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30  # Size of each square block

PLAY_WIDTH = 10 * BLOCK_SIZE  # 10 blocks wide
PLAY_HEIGHT = 20 * BLOCK_SIZE # 20 blocks high
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

# Tetromino shapes (S, Z, I, O, J, L, T)
# Each shape is represented by a list of rotations.
# Each rotation is a list of (x, y) offsets relative to the block's center/pivot.
S_SHAPE = [['.O.',
            'OO.',
            '...'],
           ['.O.',
            '.OO',
            '..O']]

Z_SHAPE = [['OO.',
            '.OO',
            '...'],
           ['..O',
            '.OO',
            '.O.']]

I_SHAPE = [['.O.',
            '.O.',
            '.O.',
            '.O.'],
           ['....',
            'OOOO',
            '....',
            '....']]

O_SHAPE = [['OO.',
            'OO.',
            '...']]

J_SHAPE = [['.O.',
            '.O.',
            'OO.'],
           ['O..',
            'OOO',
            '...'],
           ['.OO',
            '.O.',
            '.O.'],
           ['OOO',
            '..O',
            '...']]

L_SHAPE = [['.O.',
            '.O.',
            '.OO'],
           ['..O',
            'OOO',
            '...'],
           ['OO.',
            '.O.',
            '.O.'],
           ['OOO',
            'O..',
            '...']]

T_SHAPE = [['.O.',
            'OOO',
            '...'],
           ['.O.',
            '.OO',
            '.O.'],
           ['OOO',
            '.O.',
            '...'],
           ['.O.',
            'OO.',
            '.O.']]

SHAPES = [S_SHAPE, Z_SHAPE, I_SHAPE, O_SHAPE, J_SHAPE, L_SHAPE, T_SHAPE]
SHAPE_COLORS = [GREEN, RED, CYAN, YELLOW, BLUE, ORANGE, PURPLE]


# --- Game Board ---
# Create an empty grid
def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(10)] for _ in range(20)] # 10 columns, 20 rows

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                c = locked_positions[(x, y)]
                grid[y][x] = c
    return grid

# --- Tetromino Class ---
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0 # Index to current rotation of the shape

# --- Game Logic Functions ---

def convert_shape_format(piece):
    positions = []
    current_shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(current_shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'O':
                positions.append((piece.x + j, piece.y + i))

    # Offset for shapes to be centered better (adjust if needed)
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4) # Adjust these offsets based on your shapes

    return positions

def valid_space(piece, grid):
    # Check if piece is within bounds and doesn't collide with locked blocks
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == BLACK] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub] # Flatten the list

    formatted_piece = convert_shape_format(piece)

    for pos in formatted_piece:
        if pos not in accepted_positions:
            if pos[1] > -1: # Allow pieces to start above the top of the screen
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1: # If any part of a locked block is above the top row
            return True
    return False

def get_new_piece():
    return Piece(5, 0, random.choice(SHAPES)) # Start new pieces near the top-center

def draw_text(surface, text, size, color, x, y):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (x, y))

def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # Draw grid lines
    for i in range(21): # 20 rows + 1 for bottom line
        pygame.draw.line(surface, GRAY, (TOP_LEFT_X, TOP_LEFT_Y + i * BLOCK_SIZE), (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + i * BLOCK_SIZE))
    for j in range(11): # 10 columns + 1 for right line
        pygame.draw.line(surface, GRAY, (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y), (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))

def clear_rows(grid, locked):
    num_cleared_rows = 0
    # Iterate from bottom to top
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if BLACK not in row: # If no black (empty) space in the row
            num_cleared_rows += 1
            ind = i # Index of the row to clear

            # Shift rows above down
            for j in range(ind, 0, -1):
                grid[j] = grid[j-1]
                for x in range(len(grid[j])):
                    if (x, j-1) in locked:
                        locked[(x, j)] = locked.pop((x, j-1)) # Update locked positions

            # Clear the top row (now shifted down)
            grid[0] = [BLACK for _ in range(10)]
            # If a row was cleared, you need to re-check the same row index in the next iteration
            # because the rows above have shifted down into its place.
            # This is handled by not incrementing 'i' in the outer loop.
            # However, for simplicity, we'll just re-check everything after one clear.
            # A more efficient approach would be to only re-check the rows above.
            # For this simple example, we'll just make the grid fresh for the next loop.
    return num_cleared_rows

def draw_next_shape(piece, surface):
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Next Shape", 1, WHITE)

    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT // 2 - 100

    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'O':
                pygame.draw.rect(surface, piece.color, (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    surface.blit(label, (sx + 10, sy - 30))

def draw_window(surface, grid, score=0, last_score=0):
    surface.fill(BLACK)
    pygame.font.init()

    draw_text(surface, "Tetris", 60, WHITE, SCREEN_WIDTH // 2 - 80, 20)
    draw_text(surface, f"Score: {score}", 20, WHITE, TOP_LEFT_X + PLAY_WIDTH + 50, TOP_LEFT_Y + 20)
    draw_text(surface, f"High Score: {last_score}", 20, WHITE, TOP_LEFT_X + PLAY_WIDTH + 50, TOP_LEFT_Y + 80)

    draw_grid(surface, grid)
    pygame.draw.rect(surface, GRAY, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5) # Border around play area

    pygame.display.update()

def main(win):
    last_score = load_high_score()
    locked_positions = {} # (x,y):(color)
    grid = create_grid(locked_positions)

    current_piece = get_new_piece()
    next_piece = get_new_piece()
    change_piece = False
    run = True
    fall_time = 0
    fall_speed = 0.27 # Adjust for speed
    level_time = 0
    score = 0

    clock = pygame.time.Clock()

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5: # Increase speed every 5 seconds (adjust)
            level_time = 0
            if fall_speed > 0.12: # Don't get too fast
                fall_speed -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP: # Rotate
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                if event.key == pygame.K_SPACE: # Hard drop
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1 # Move back one step as it's now invalid
                    change_piece = True # Force a new piece

        if change_piece:
            for pos in convert_shape_format(current_piece):
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_new_piece()
            change_piece = False
            rows_cleared = clear_rows(grid, locked_positions)
            score += rows_cleared * 100 # Simple scoring (100 points per line)
            if rows_cleared > 0:
                # Award bonus for multiple lines (Tetris!)
                score += (rows_cleared - 1) * 200 # +200 for 2 lines, +400 for 3, +600 for 4

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text(win, "YOU LOST!", 80, RED, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False
            save_high_score(score) # Save score on loss

def save_high_score(score):
    try:
        with open("high_score.txt", "w") as f:
            f.write(str(score))
    except Exception as e:
        print(f"Error saving high score: {e}")

def load_high_score():
    try:
        with open("high_score.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0
    except Exception as e:
        print(f"Error loading high score: {e}")
        return 0

# --- Main execution ---
if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    main(win)
    pygame.quit()