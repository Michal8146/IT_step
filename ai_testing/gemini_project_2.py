import pygame
import random
import os # For file operations (high score)

# --- Constants ---
SCREEN_WIDTH = 500  # Increased width to accommodate next piece and score display
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30  # Size of each square block

PLAY_WIDTH = 10 * BLOCK_SIZE  # 10 blocks wide
PLAY_HEIGHT = 20 * BLOCK_SIZE # 20 blocks high

# Calculate top-left corner of the play area to center it horizontally
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT

# Colors (RGB tuples)
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
# Each rotation is a list of strings, where 'O' represents a filled block
# and '.' represents an empty space.
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


# --- Game Board / Grid ---
# Creates an empty grid or populates it with locked positions
def create_grid(locked_positions={}):
    # Initialize a 20x10 grid with BLACK (empty) cells
    grid = [[BLACK for _ in range(10)] for _ in range(20)]

    # Fill in locked positions with their respective colors
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                c = locked_positions[(x, y)]
                grid[y][x] = c
    return grid

# --- Tetromino Piece Class ---
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0 # Index to current rotation of the shape

# --- Game Logic Helper Functions ---

# Converts the 'O' and '.' shape format into actual (x, y) grid coordinates
def convert_shape_format(piece):
    positions = []
    # Get the current rotation of the shape
    current_shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(current_shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'O':
                # Calculate absolute grid position
                positions.append((piece.x + j, piece.y + i))

    # Adjust for shapes to be centered better (important for how they appear initially)
    # These offsets might need fine-tuning if you change your shape definitions
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4) # Adjust these offsets based on your shapes
                                               # -2 for horizontal centering on 10-block grid
                                               # -4 to allow pieces to start slightly above grid (y=0 is first row)

    return positions

# Checks if a piece can move to a given position without collision
def valid_space(piece, grid):
    # Create a flattened list of all empty (BLACK) positions on the grid
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == BLACK] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub] # Flatten the list

    formatted_piece = convert_shape_format(piece)

    for pos in formatted_piece:
        x, y = pos
        if (x, y) not in accepted_positions: # If proposed position is not empty
            # Check if it's out of bounds (left, right, bottom)
            if y > -1 and x >= 0 and x < 10 and y < 20: # If within vertical bounds of play area
                return False # Collision with a locked block or boundary
            elif y >= 20: # Collision with bottom of the play area
                return False
            # Allow pieces to start above the top of the screen (y < 0)
            # This is why the 'if y > -1' is there. If y is -1 or -2, it's considered valid
            # as long as x is in bounds.
            elif not (x >= 0 and x < 10): # Check horizontal bounds even for y < 0
                 return False

    return True

# Checks if any locked blocks are above the visible play area (game over condition)
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1: # If any part of a locked block is on or above the top visible row (row 0)
            return True
    return False

# Returns a new randomly selected Tetromino piece
def get_new_piece():
    # Start new pieces near the top-center of the grid (x=5 is center, y=0 is top row)
    return Piece(5, 0, random.choice(SHAPES))

# --- Drawing Functions ---

# Draws text on the screen
def draw_text(surface, text, size, color, x, y):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (x, y))

# Draws the grid, including settled blocks
def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            # Draw each block as a filled rectangle
            pygame.draw.rect(surface, grid[y][x],
                             (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + y * BLOCK_SIZE,
                              BLOCK_SIZE, BLOCK_SIZE), 0)

    # Draw grid lines for visual clarity
    for i in range(21): # 20 rows + 1 for bottom line
        pygame.draw.line(surface, GRAY, (TOP_LEFT_X, TOP_LEFT_Y + i * BLOCK_SIZE),
                         (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + i * BLOCK_SIZE))
    for j in range(11): # 10 columns + 1 for right line
        pygame.draw.line(surface, GRAY, (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y),
                         (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))

# Draws the actively falling piece
def draw_piece(surface, piece):
    formatted_piece = convert_shape_format(piece)
    for pos in formatted_piece:
        x, y = pos
        # Only draw the block if its y-coordinate is within the visible play area
        # (i.e., not above the top of the grid, where y would be negative)
        if y >= 0:
            pygame.draw.rect(surface, piece.color,
                             (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + y * BLOCK_SIZE,
                              BLOCK_SIZE, BLOCK_SIZE), 0)

# Clears full rows and shifts blocks down
def clear_rows(grid, locked):
    num_cleared_rows = 0
    # Iterate from the bottom of the grid upwards
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if BLACK not in row: # If the row has no empty (black) spaces, it's full
            num_cleared_rows += 1
            ind = i # Store the index of the row to clear

            # Remove entries for the cleared row from locked_positions
            for j in range(len(row)):
                if (j, ind) in locked:
                    del locked[(j, ind)]

            # Shift rows above down:
            # Iterate from the cleared row's index upwards to the top
            for j in range(ind, 0, -1):
                # Copy the row above down to the current row
                grid[j] = grid[j-1]
                # Update the y-coordinates in locked_positions for affected blocks
                for x in range(len(grid[j])):
                    if (x, j-1) in locked:
                        locked[(x, j)] = locked.pop((x, j-1)) # Move (x, j-1) to (x, j)

            # After shifting, the top row is now a copy of the second row, etc.
            # The very top row (index 0) becomes empty.
            grid[0] = [BLACK for _ in range(10)]
    return num_cleared_rows

# Draws the next shape preview on the side
def draw_next_shape(piece, surface):
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Next Shape", 1, WHITE)

    # Position for the next shape display, to the right of the play area
    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT // 2 - 100 # Adjust vertically for centering

    # Get the current (first) rotation of the next piece
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'O':
                pygame.draw.rect(surface, piece.color,
                                 (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE), 0)

    surface.blit(label, (sx + 10, sy - 30)) # Position the "Next Shape" text

# Draws the entire game window (background, score, grid, border)
def draw_window(surface, grid, score=0, last_score=0):
    surface.fill(BLACK) # Fill the entire screen black first
    pygame.font.init() # Initialize font module (good practice to do it once, but safe here)

    # Draw title
    draw_text(surface, "TETRIS", 60, WHITE, SCREEN_WIDTH // 2 - 80, 20)

    # Draw score and high score
    draw_text(surface, f"Score: {score}", 20, WHITE, TOP_LEFT_X + PLAY_WIDTH + 50, TOP_LEFT_Y + 20)
    draw_text(surface, f"High Score: {last_score}", 20, WHITE, TOP_LEFT_X + PLAY_WIDTH + 50, TOP_LEFT_Y + 80)

    # Draw the main game grid (locked blocks and empty spaces)
    draw_grid(surface, grid)

    # Draw a border around the play area
    pygame.draw.rect(surface, GRAY, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5) # 5 pixels thick border

    # Note: pygame.display.update() is called outside this function in the main loop
    # to ensure all elements (including the falling piece) are drawn before update.

# --- High Score Management ---
HIGH_SCORE_FILE = "high_score.txt"

def save_high_score(score):
    try:
        # Check if file exists, if not, create it
        if not os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, "w") as f:
                f.write("0") # Initialize with 0 if file doesn't exist

        # Read current high score
        current_high_score = load_high_score()

        # If new score is higher, save it
        if score > current_high_score:
            with open(HIGH_SCORE_FILE, "w") as f:
                f.write(str(score))
    except Exception as e:
        print(f"Error saving high score: {e}")

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    except FileNotFoundError:
        # If file doesn't exist, return 0 (no high score yet)
        return 0
    except ValueError:
        # If file content is not a valid integer, return 0 and possibly reset
        print(f"Warning: High score file '{HIGH_SCORE_FILE}' corrupted. Resetting to 0.")
        return 0
    except Exception as e:
        print(f"Error loading high score: {e}")
        return 0


# --- Main Game Loop ---
def main(win):
    last_score = load_high_score() # Load high score at the start of the game
    locked_positions = {} # Dictionary to store (x,y):(color) for landed blocks
    grid = create_grid(locked_positions)

    current_piece = get_new_piece()
    next_piece = get_new_piece()
    change_piece = False # Flag to indicate if a new piece should be generated
    run = True
    fall_time = 0 # Time since last fall
    fall_speed = 0.27 # How fast the piece falls (seconds per block)
    level_time = 0 # Time to increase difficulty
    score = 0

    clock = pygame.time.Clock() # Pygame clock to control frame rate

    while run:
        # Re-create the grid each frame, integrating locked_positions
        grid = create_grid(locked_positions)

        # Calculate time passed since last frame
        fall_time += clock.get_rawtime() # Raw time is milliseconds since last tick
        level_time += clock.get_rawtime()
        clock.tick() # Advance the clock and cap FPS (e.g., to 60 by default)

        # Increase fall speed over time to increase difficulty
        if level_time / 1000 > 10: # Every 10 seconds (adjust as desired)
            level_time = 0
            if fall_speed > 0.12: # Don't let it get ridiculously fast
                fall_speed -= 0.005 # Make it fall slightly faster

        # Automatic falling logic
        if fall_time / 1000 > fall_speed: # If enough time has passed
            fall_time = 0
            current_piece.y += 1 # Move piece down one block
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                # If the piece is now invalid (collided) and not starting above the grid
                current_piece.y -= 1 # Move it back up
                change_piece = True # Mark for new piece generation

        # Event handling (user input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False # Exit game loop if window is closed
                pygame.display.quit()
                quit() # Quit Pygame and Python

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1 # Move back if invalid
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1 # Move back if invalid
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1 # Move back if invalid
                if event.key == pygame.K_UP: # Rotate (typically 'Up' arrow)
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape) # Revert rotation if invalid
                if event.key == pygame.K_SPACE: # Hard drop
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1 # Move back one step as it's now invalid after the loop
                    change_piece = True # Force a new piece

        # Logic for when a piece has landed
        if change_piece:
            # Add the current piece's blocks to locked_positions
            for pos in convert_shape_format(current_piece):
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color

            # Get the next piece
            current_piece = next_piece
            next_piece = get_new_piece()
            change_piece = False # Reset flag

            # Clear any full rows
            rows_cleared = clear_rows(grid, locked_positions)
            # Scoring: 100 points per line, plus bonus for multiple lines
            if rows_cleared == 1:
                score += 100
            elif rows_cleared == 2:
                score += 300 # 100 + 200 bonus
            elif rows_cleared == 3:
                score += 500 # 100 + 400 bonus
            elif rows_cleared == 4: # TETRIS!
                score += 800 # 100 + 700 bonus

        # --- Drawing calls ---
        draw_window(win, grid, score, last_score) # Draws background, score, locked blocks, grid lines
        draw_next_shape(next_piece, win)          # Draws the preview of the next piece
        draw_piece(win, current_piece)            # Draws the actively falling piece

        pygame.display.update() # Update the entire screen to show everything drawn

        # Check for game over
        if check_lost(locked_positions):
            draw_text(win, "YOU LOST!", 80, RED, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50)
            pygame.display.update()
            pygame.time.delay(2000) # Show "YOU LOST!" for 2 seconds
            run = False # Exit game loop
            save_high_score(score) # Save score when game ends

# --- Initialization and Game Start ---
if __name__ == '__main__':
    pygame.init() # Initialize all the Pygame modules
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Create the display surface
    pygame.display.set_caption('Tetris') # Set window title
    main(win) # Start the main game loop
    pygame.quit() # Uninitialize Pygame modules when game ends