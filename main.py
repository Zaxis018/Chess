import pygame
import utils

# Initialize Pygame
pygame.init()

# Set the display for the game
width = 800
height = 800
size = (width, height)
screen = pygame.display.set_mode(size)

# Set the cell size and create a surface for the board
cellSize = width / 8
board = pygame.Surface((cellSize * 8, cellSize * 8))

# Fill the board with a custom color
board.fill((200, 200, 200))  # white first

# Draw the black cells on the board
for x in range(0, 8, 2):
    for y in range(0, 8, 2):
        pygame.draw.rect(board, (0, 0, 0), (x * cellSize, y * cellSize, cellSize, cellSize))
        pygame.draw.rect(board, (100, 100, 100), ((x + 1) * cellSize, (y + 1) * cellSize, cellSize, cellSize))

# Initialize an empty 8x8 chessboard
chessboard = [[None] * 8 for _ in range(8)]

# Initialize an empty 8x8 chessboard with starting piece positions
chessboard = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], #0th row
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]  #7th row
]   #0th column                                7th
print(chessboard[7][1])
# Load PNG images stored in the images folder
IMAGES = {}
pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
for piece in pieces:
    IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (int(cellSize), int(cellSize)))

move_count = 0
selected_piece = None  # Variable to keep track of the selected piece
selected_square = None  # Variable to keep track of the selected square

# Draw the board surface first
utils.draw_pieces(screen, board, chessboard, IMAGES, cellSize)


def is_valid_move(source, destination, piece):
    # Extract the source and destination coordinates
    source_x, source_y = source
    dest_x, dest_y = destination

    # Ensure the source and destination are within the chessboard bounds
    if not (0 <= source_x < 8) or not (0 <= source_y < 8) or not (0 <= dest_x < 8) or not (0 <= dest_y < 8):
        return False

    # Check if the source and destination squares are the same
    if source == destination:
        return False

    # Check if the destination square is occupied by a piece of the same color
    if chessboard[dest_y][dest_x] is not None and chessboard[dest_y][dest_x][0] == piece[0]:# why y,x instead of x,y
        return False

    # Check if the move is valid for the specific piece type
    if piece[1] == 'P':
        return is_valid_pawn_move(source, destination, piece)
    elif piece[1] == 'R':
        return is_valid_rook_move(source, destination)
    elif piece[1] == 'N':
        return is_valid_knight_move(source, destination)
    elif piece[1] == 'B':
        return is_valid_bishop_move(source, destination)
    elif piece[1] == 'Q':
        return is_valid_queen_move(source, destination)
    elif piece[1] == 'K':
        return is_valid_king_move(source, destination)

    return False


def is_valid_pawn_move(source, destination, piece):
    source_x, source_y = source
    dest_x, dest_y = destination

    # Determine the direction of the pawn based on its color
    direction = -1 if piece[0] == 'w' else 1

    # Pawns can move one square forward
    if source_x == dest_x and source_y + direction == dest_y:
        return True

    # Pawns can move two squares forward on their first move
    if source_x == dest_x and source_y + (2 * direction) == dest_y and source_y == 6 and piece[0] == 'w':
        return True
    if source_x == dest_x and source_y + (2 * direction) == dest_y and source_y == 1 and piece[0] == 'b':
        return True

    # Pawns can capture diagonally
    if abs(source_x - dest_x) == 1 and source_y + direction == dest_y and chessboard[dest_y][dest_x] is not None:
        return True

    else :
        return False

# Implement the remaining piece move validation functions (Rook, Knight, Bishop, Queen, King) as per the rules of chess.

def is_valid_rook_move(source, destination):
    source_x,source_y=source
    dest_x,dest_y=destination
    if source_x!=dest_x and source_y!=dest_y: #cant change both x and y at same time ie only straight
        return False
    # Check if the path is clear (no pieces in the way)
    path_squares = utils.tracepath(source, destination)
    for square in path_squares:
        x, y = square
        if chessboard[y][x] is not None:
            return False  # There's a piece in the way
    return True  

def is_valid_knight_move(source, destination):
    source_x, source_y = source
    dest_x, dest_y = destination

    # Check if the move is an L-shape
    x_diff = abs(dest_x - source_x)
    y_diff = abs(dest_y - source_y)

    if (x_diff == 1 and y_diff == 2) or (x_diff == 2 and y_diff == 1):
        return True
    else:
        return False

def is_valid_bishop_move(source, destination):
    source_x,source_y=source
    dest_x,dest_y=destination
    if not abs(source_x - dest_x) == abs(source_y - dest_y):#checks diagonality 

        return False
    # Check if the path is clear (no pieces in the way)
    path_squares = utils.tracepath(source, destination)
    for square in path_squares:
        x, y = square
        if chessboard[y][x] is not None:
            return False
    return True  # Replace with your implementation

def is_valid_queen_move(source, destination):
    source_x, source_y = source
    dest_x, dest_y = destination

    # Check if it's a valid rook or bishop move
    rook_condition = source_x == dest_x or source_y == dest_y
    bishop_condition = abs(source_x - dest_x) == abs(source_y - dest_y)

    if rook_condition or bishop_condition:
        # Check if the path is clear (no pieces in the way)
        path_squares = utils.tracepath(source, destination)
        for square in path_squares:
            x, y = square
            if chessboard[y][x] is not None:
                return False  # There's a piece in the way
        return True
    else:
        return False


def is_valid_king_move(source, destination):
    source_x, source_y = source
    dest_x, dest_y = destination

    # Check if the move is within one square in any direction
    x_diff = abs(dest_x - source_x)
    y_diff = abs(dest_y - source_y)

    if x_diff <= 1 and y_diff <= 1:
        return True
    else:
        return False


def is_players_turn(piece, move_count):
    # Check if it's White's turn (even move count) and the piece is a white piece
    if move_count % 2 == 0 and piece[0] == 'w':
        return True
    # Check if it's Black's turn (odd move count) and the piece is a black piece
    elif move_count % 2 == 1 and piece[0] == 'b':
        return True
    else:
        return False
    

def highlight_square(screen, selected_square, cellSize,highlight_color):
    # Extract the row and column from selected_square
    row, col = selected_square

    # Calculate the position and size of the highlighted square
    x = (row) * cellSize
    y = (col)* cellSize
    width = cellSize
    height = cellSize

    # # Define the highlight color (e.g., red)
    # highlight_color

    # Draw a rectangle to highlight the square
    pygame.draw.rect(screen, highlight_color, (x, y, width, height), 3)  # 3 is the border width


def highlight_valid_moves(screen, selected_piece, selected_square, cellSize):
    for row in range(8):
        for col in range(8):
            destination_square = (col, row)
            if is_valid_move(selected_square, destination_square, selected_piece):
                highlight_square(screen, destination_square, cellSize, highlight_color=(0, 255, 0))

def clear_highlights(screen, cellSize):
    for row in range(8):
        for col in range(8):
            square = (col, row)
            highlight_square(screen, square, cellSize, highlight_color=(255, 255, 255))  # Use the background color to "clear" the highlight


#print(chessboard)

# Game loop
selecting_piece = True  # Initially, the player is selecting a piece
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos  # Get mouse click position
            clicked_square = utils.get_square(event, cellSize, x, y)

            if selecting_piece and event.button==1:
                # If the player is currently selecting a piece, check if the clicked square contains a piece
                piece = chessboard[clicked_square[1]][clicked_square[0]]# why working on 1,o instead of 0,1?
                if piece is not None and is_players_turn(piece, move_count):
                    # Select the piece
                    selected_piece = piece
                    selected_square = clicked_square
                    # Highlight the selected square with a different color
                    highlight_square(screen, selected_square, cellSize,highlight_color=(255, 0, 0))
                    highlight_valid_moves(screen, selected_piece, selected_square, cellSize)
                    selecting_piece = False  # Move to the state of selecting the destination square
                else:
                    # If no piece is selected, do nothing
                    pass
            elif not selecting_piece: 
                # If the player is currently selecting a destination square, this is the destination square
                destination_square = clicked_square
                if is_valid_move(selected_square, destination_square, selected_piece):
                    # Update the board state with the new move
                    chessboard[destination_square[1]][destination_square[0]] = selected_piece
                    chessboard[selected_square[1]][selected_square[0]] = None
                    print(chessboard)
                    move_count += 1  # Increment the move count
                    clear_highlights(screen, cellSize)  # Clear highlights after the move

                # Clear the selected piece and squares
                selected_piece = None
                selected_square = None
                destination_square = None
                selecting_piece = True  # Move back to the state of selecting a piece

                    # Draw the board with the updated piece positions
                utils.draw_pieces(screen, board, chessboard, IMAGES, cellSize)


    # # Draw the board with the updated piece positions
    # utils.draw_pieces(screen, board, chessboard, IMAGES, cellSize)

    # Update the display
    pygame.display.update()