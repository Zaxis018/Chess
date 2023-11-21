import pygame
from pygame.locals import *

def is_square_under_attack(chessboard, square, color):
    opponent_color = 'b' if color == 'w' else 'w'
    for y in range(8):
        for x in range(8):
            piece = chessboard[y][x]
            if piece is not None and piece[0] == opponent_color:
                if is_opponent_attacking_king(chessboard, (x, y), square, piece):
                    return True  # The square is under attack
    return False


def is_valid_castling(chessboard, source, destination, piece):
    source_x, source_y = source
    dest_x, dest_y = destination
    color = piece[0]
    if is_king_in_check(chessboard, color):
        return False
    # Check if the king and rook involved in castling have not moved
    if piece[1] == 'K' and source_x == 4:
        if piece[0] == 'w':
            # White king
            if dest_x == 6 and dest_y == 7 and  has_white_king_moved==False and  has_white_king_side_rook_moved==False:
                # White kingside castling
                for x in range(source_x + 1, dest_x):
                    if chessboard[source_y][x] is not None or is_square_under_attack(chessboard, (x, source_y), piece[0]):
                        return False  # There's a piece in the way or the king is under attack
                return all(chessboard[source_y][x] is None for x in range(dest_x + 1, 7)) and \
                       not is_square_under_attack(chessboard, (dest_x, source_y), piece[0]) and \
                       not is_square_under_attack(chessboard, (dest_x - 1, source_y), piece[0])  # Check if there are no pieces between king and rook

            elif dest_x == 2 and dest_y == 7 and not has_white_king_moved and not has_white_queen_side_rook_moved:
                # White queenside castling
                for x in range(dest_x + 1, source_x):
                    if chessboard[source_y][x] is not None or is_square_under_attack(chessboard, (x, source_y), piece[0]):
                        return False  # There's a piece in the way or the king is under attack
                return all(chessboard[source_y][x] is None for x in range(1, dest_x)) and \
                       not is_square_under_attack(chessboard, (dest_x, source_y), piece[0]) and \
                       not is_square_under_attack(chessboard, (dest_x + 1, source_y), piece[0])  # Check if there are no pieces between king and rook

        elif piece[0] == 'b':
            # Black king
            if dest_x == 6 and dest_y == 0 and not has_black_king_moved and not has_black_king_side_rook_moved:
                # Black kingside castling
                for x in range(source_x + 1, dest_x):
                    if chessboard[source_y][x] is not None or is_square_under_attack(chessboard, (x, source_y), piece[0]):
                        return False  # There's a piece in the way or the king is under attack
                return all(chessboard[source_y][x] is None for x in range(dest_x + 1, 7)) and \
                       not is_square_under_attack(chessboard, (dest_x, source_y), piece[0]) and \
                       not is_square_under_attack(chessboard, (dest_x - 1, source_y), piece[0])  # Check if there are no pieces between king and rook

            elif dest_x == 2 and dest_y == 0 and not has_black_king_moved and not has_black_queen_side_rook_moved:
                # Black queenside castling
                for x in range(dest_x + 1, source_x):
                    if chessboard[source_y][x] is not None or is_square_under_attack(chessboard, (x, source_y), piece[0]):
                        return False  # There's a piece in the way or the king is under attack
                return all(chessboard[source_y][x] is None for x in range(1, dest_x)) and \
                       not is_square_under_attack(chessboard, (dest_x, source_y), piece[0]) and \
                       not is_square_under_attack(chessboard, (dest_x + 1, source_y), piece[0])  # Check if there are no pieces between king and rook

    return False


def perform_castling(chessboard, source, destination, piece,move_count):
    source_x, source_y = source
    dest_x, dest_y = destination

    # Update the positions of the king and rook after castling
    if dest_x == 6:  # Kingside castling
        chessboard[source_y][dest_x] = piece
        chessboard[source_y][source_x] = None  # Clear the original king position
        chessboard[source_y][5] = chessboard[source_y][7]  # Move the rook
        chessboard[source_y][7] = None  # Clear the original rook position
    elif dest_x == 2:  # Queenside castling
        chessboard[source_y][dest_x] = piece
        chessboard[source_y][source_x] = None  # Clear the original king position
        chessboard[source_y][3] = chessboard[source_y][0]  # Move the rook
        chessboard[source_y][0] = None  # Clear the original rook position
        # Update the move count
    move_count=move_count+1 
    return move_count


def is_valid_en_passant(chessboard, source, destination, piece, en_passant_square):
    source_x, source_y = source
    dest_x, dest_y = destination
    # Simulate the move to check if the king is in check after the move
    simulated_chessboard = [row[:] for row in chessboard]
    simulated_chessboard[dest_y][dest_x] = simulated_chessboard[source_y][source_x]
    simulated_chessboard[source_y][source_x] = None

    king_color = piece[0]
    if is_king_in_check(simulated_chessboard, king_color):
        return False  # Move puts the king in check
    direction = -1 if piece[0] == 'w' else 1
    color = piece[0]
    if is_king_in_check(chessboard, color):
        return False
   
    if en_passant_square is not None and  source_y==(en_passant_square[1]-direction)and abs(source_x - en_passant_square[0]) == 1 and dest_x == en_passant_square[0] and dest_y == en_passant_square[1] :
        return True

    return False

def perform_en_passant(chessboard, source, destination, piece, en_passant_square):
    dest_x, dest_y = destination
    direction = -1 if piece[0] == 'w' else 1
    # Capture the pawn that is being attacked en passant
    captured_pawn_square = (dest_x, en_passant_square[1]-direction)
    chessboard[captured_pawn_square[1]][captured_pawn_square[0]] = None

    # Move the attacking pawn to the destination square
    chessboard[dest_y][dest_x] = piece
    chessboard[source[1]][source[0]] = None



def get_square(event, cellSize, x_pos, y_pos):
    if event.button == 1:  # Left mouse button
        x = x_pos
        y = y_pos
        # print(f"Left click at ({x}, {y})")
        # Logic to find out which square is the mouse clicked on
        clicked_square = (int(x // cellSize), int(y // cellSize))
        # print(clicked_square)
        return clicked_square
    
def draw_pieces(screen,board,chessboard,IMAGES,cellSize):
    screen.blit(board, board.get_rect())
    for i in range(8):
        for j in range(8):
            piece = chessboard[i][j]
            if piece is not None:
                screen.blit(IMAGES[piece], pygame.Rect(j*cellSize, i*cellSize, cellSize, cellSize))

def tracepath(source, destination):
    source_x, source_y = source
    dest_x, dest_y = destination
    path_squares = []  # to store squares

    if source_x == dest_x:  # vertical path
        start_y, end_y = (source_y + 1, dest_y) if dest_y > source_y else (dest_y + 1, source_y)
        for y in range(start_y, end_y):
            square = (source_x, y)
            path_squares.append(square)

    elif source_y == dest_y:  # horizontal path
        start_x, end_x = (source_x + 1, dest_x) if dest_x > source_x else (dest_x + 1, source_x)
        for x in range(start_x, end_x):
            square = (x, source_y)
            path_squares.append(square)


    elif source_x != dest_x and source_y != dest_y:  # diagonal path not applicable for horse
        # Determine the direction of movement
        direction_x = 1 if dest_x > source_x else -1
        direction_y = 1 if dest_y > source_y else -1

        for i in range(1, abs(dest_x - source_x)):
            square = (source_x + i * direction_x, source_y + i * direction_y)
            path_squares.append(square)

    return path_squares


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
    pygame.draw.rect(screen, highlight_color, (x, y, width, height), 5)  # 3 is the border width


def highlight_valid_moves(chessboard,screen, selected_piece, selected_square, cellSize):
    for row in range(8):
        for col in range(8):
            destination_square = (col, row)
            if is_valid_move(chessboard,selected_square, destination_square, selected_piece,en_passant_square):
                highlight_square(screen, destination_square, cellSize, highlight_color=(0, 255, 0))


def clear_highlights(screen, cellSize):
    for row in range(8):
        for col in range(8):
            square = (col, row)
            highlight_square(screen, square, cellSize, highlight_color=(255, 255, 255))  # Use the background color to "clear" the highlight


def promote_pawn(screen, cellSize, width, height, player_color):
    font = pygame.font.Font(None, 36)
    text = font.render("Pawn Promotion", True, (255, 255, 255))
    screen.blit(text, (width // 2 +150, height // 2 - 50))
    pygame.display.flip()

    promotion_options = ['Queen', 'Rook', 'Bishop', 'Night']
    option_rects = []

    piece_images = {
        'Queen': pygame.transform.scale(pygame.image.load(f'images/{player_color}Q.png'), (100, 100)),
        'Rook': pygame.transform.scale(pygame.image.load(f'images/{player_color}R.png'), (100, 100)),
        'Bishop': pygame.transform.scale(pygame.image.load(f'images/{player_color}B.png'), (100, 100)),
        'Night': pygame.transform.scale(pygame.image.load(f'images/{player_color}N.png'), (100, 100)),
    }

    for i, option in enumerate(promotion_options):
        rect = pygame.Rect(width // 2 - 50 + i * 100, height // 2, 100, 100)
        pygame.draw.rect(screen, (0, 0, 255), rect, 2)
        option_rects.append(rect)
        screen.blit(piece_images[option], (rect.x + 10, rect.y + 10))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(x, y):
                        return promotion_options[i]
# Initialize Pygame
def is_valid_move(chessboard, source, destination, piece, en_passant_square):
    # Extract the source and destination coordinates
    source_x, source_y = source
    dest_x, dest_y = destination

    # Ensure the source and destination squares are within the chessboard bounds
    if not (0 <= source_x < 8) or not (0 <= source_y < 8) or not (0 <= dest_x < 8) or not (0 <= dest_y < 8):
        return False

    # Check if the source and destination squares are the same
    if source == destination:
        return False

    # Check if the destination square is occupied by a piece of the same color
    if chessboard[dest_y][dest_x] is not None and chessboard[dest_y][dest_x][0] == piece[0]:
        return False

    # Check if it's a valid castling move
    if piece[1] == 'K' and is_valid_castling(chessboard, source, destination, piece):
        return True
    if piece[1]=='P' and is_valid_en_passant(chessboard, source, destination, piece, en_passant_square):
        return True

    # Check if the move is valid for the specific piece type
    if piece[1] == 'P':
        valid_move = is_valid_pawn_move(chessboard, source, destination, piece,en_passant_square)
    elif piece[1] == 'R':
        valid_move = is_valid_rook_move(chessboard, source, destination)
    elif piece[1] == 'N':
        valid_move = is_valid_knight_move(source, destination)
    elif piece[1] == 'B':
        valid_move = is_valid_bishop_move(chessboard, source, destination)
    elif piece[1] == 'Q':
        valid_move = is_valid_queen_move(chessboard, source, destination)
    elif piece[1] == 'K':
        valid_move = is_valid_king_move(chessboard, source, destination)

    if not valid_move:
        return False

    # Simulate the move to check if the king is in check after the move
    simulated_chessboard = [row[:] for row in chessboard]
    simulated_chessboard[dest_y][dest_x] = simulated_chessboard[source_y][source_x]
    simulated_chessboard[source_y][source_x] = None

    king_color = piece[0]
    if is_king_in_check(simulated_chessboard, king_color):
        return False  # Move puts the king in check

    return True


def is_king_in_check(chessboard, color):
    # Find the king's position
    king_position = find_king_position(chessboard, color)

    # Check if any opponent's piece can attack the king
    opponent_color = 'b' if color == 'w' else 'w'
    for y in range(8):
        for x in range(8):
            piece = chessboard[y][x]
            if piece is not None and piece[0] == opponent_color:
                if is_opponent_attacking_king(chessboard, (x, y), king_position, piece):
                    return True  # King is in check

    return False

def find_king_position(chessboard, color):
    for y in range(8):
        for x in range(8):
            piece = chessboard[y][x]
            if piece is not None and piece[0] == color and piece[1] == 'K':
                return (x, y)

def is_opponent_attacking_king(chessboard, opponent_position, king_position, opponent_piece):
    # Check if the opponent's piece can attack the king
    if opponent_piece[1] == 'P':
        return is_valid_pawn_move(chessboard, opponent_position, king_position, opponent_piece,en_passant_square)
    elif opponent_piece[1] == 'R':
        return is_valid_rook_move(chessboard, opponent_position, king_position)
    elif opponent_piece[1] == 'N':
        return is_valid_knight_move(opponent_position, king_position)
    elif opponent_piece[1] == 'B':
        return is_valid_bishop_move(chessboard, opponent_position, king_position)
    elif opponent_piece[1] == 'Q':
        return is_valid_queen_move(chessboard, opponent_position, king_position)
    elif opponent_piece[1] == 'K':
        return is_valid_king_move(chessboard, opponent_position, king_position)

def is_valid_pawn_move(chessboard,source, destination, piece,en_passant_square):
    source_x, source_y = source
    dest_x, dest_y = destination

    # path_squares = utils.tracepath(source, destination)
    # for square in path_squares:
    #     x, y = square
    #     if chessboard[y][x] is not None:
    #         return False  # There's a piece in the way

    # Determine the direction of the pawn based on its color
    direction = -1 if piece[0] == 'w' else 1

    # Pawns can move one square forward
    if source_x == dest_x and source_y + direction == dest_y and chessboard[dest_y][dest_x]==None:
        return True

    # Pawns can move two squares forward on their first move
    if source_x == dest_x and source_y + (2 * direction) == dest_y and source_y == 6 and piece[0] == 'w' and chessboard[dest_y][dest_x]==None and chessboard[source_y+direction][source_x]==None:
        return True
    if source_x == dest_x and source_y + (2 * direction) == dest_y and source_y == 1 and piece[0] == 'b' and chessboard[dest_y][dest_x]==None and chessboard[source_y+direction][source_x]==None:
        return True

    # Pawns can capture diagonally
    if abs(source_x - dest_x) == 1 and source_y + direction == dest_y and chessboard[dest_y][dest_x] is not None:
        return True

    else :
        return False


# Implement the remaining piece move validation functions (Rook, Knight, Bishop, Queen, King) as per the rules of chess.

def is_valid_rook_move(chessboard,source, destination):
    source_x,source_y=source
    dest_x,dest_y=destination
    if source_x!=dest_x and source_y!=dest_y: #cant change both x and y at same time ie only straight
        return False
    # Check if the path is clear (no pieces in the way)
    path_squares = tracepath(source, destination)
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

def is_valid_bishop_move(chessboard,source, destination):
    source_x,source_y=source
    dest_x,dest_y=destination
    if not abs(source_x - dest_x) == abs(source_y - dest_y):#checks diagonality 

        return False
    # Check if the path is clear (no pieces in the way)
    path_squares = tracepath(source, destination)
    for square in path_squares:
        x, y = square
        if chessboard[y][x] is not None:
            return False
    return True  # Replace with your implementation  

def is_valid_queen_move(chessboard,source, destination):
    source_x, source_y = source
    dest_x, dest_y = destination

    # Check if it's a valid rook or bishop move
    rook_condition = source_x == dest_x or source_y == dest_y
    bishop_condition = abs(source_x - dest_x) == abs(source_y - dest_y)

    if rook_condition or bishop_condition:
        # Check if the path is clear (no pieces in the way)
        path_squares =tracepath(source, destination)
        for square in path_squares:
            x, y = square
            if chessboard[y][x] is not None:
                return False  # There's a piece in the way
        return True
    else:
        return False


def is_valid_king_move(chessboard,source, destination):
    source_x, source_y = source
    dest_x, dest_y = destination

    # Check if the move is within one square in any direction
    x_diff = abs(dest_x - source_x)
    y_diff = abs(dest_y - source_y)

    if x_diff <= 1 and y_diff <= 1:
        return True
    else:
        return False



def check_valid_moves(chessboard, player): #checks if valid moves are left to see if game is over
    for y in range(8):
        for x in range(8):
            piece = chessboard[y][x]
            if piece is not None and piece[0] == player:
                for dest_y in range(8):
                    for dest_x in range(8):
                        destination = (dest_x, dest_y)
                        if is_valid_move(chessboard, (x, y), destination, piece,en_passant_square):
                            return True  # At least one valid move found for the player
    return False  # No valid moves found for the player


def is_game_over(chessboard, player_color):
    # Check if there are any valid moves for the given player
    for y in range(8):
        for x in range(8):
            piece = chessboard[y][x]
            if piece is not None and piece[0] == player_color:
                for dest_y in range(8):
                    for dest_x in range(8):
                        if is_valid_move(chessboard, (x, y), (dest_x, dest_y), piece):
                            return False  # There is at least one valid move

    return True  # No valid moves for any piece, game over

pygame.init()

# Set the display for the game
width = 800
height = 800
size = (width, height)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Chess")

# Set the cell size and create a surface for the board
cellSize = width / 8
board = pygame.Surface((cellSize * 8, cellSize * 8))

# Fill the board with a custom color
board.fill((0, 0, 50))  # white first

# Draw the black cells on the board
for x in range(0, 8, 2):
    for y in range(0, 8, 2):
        pygame.draw.rect(board, (39, 158, 103), (x * cellSize, y * cellSize, cellSize, cellSize))
        pygame.draw.rect(board, (30,98, 66), ((x + 1) * cellSize, (y + 1) * cellSize, cellSize, cellSize))

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
draw_pieces(screen, board, chessboard, IMAGES, cellSize)

#print(chessboard)

has_white_king_moved = False
has_white_king_side_rook_moved = False
has_white_queen_side_rook_moved = False

has_black_king_moved = False
has_black_king_side_rook_moved = False
has_black_queen_side_rook_moved = False
en_passant_square = None

# Game loop
selecting_piece = True  # Initially, the player is selecting a piece
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos  # Get mouse click position
            clicked_square = get_square(event, cellSize, x, y)

            if selecting_piece and event.button==1:
                # If the player is currently selecting a piece, check if the clicked square contains a piece
                piece = chessboard[clicked_square[1]][clicked_square[0]]# why working on 1,o instead of 0,1?
                if piece is not None and is_players_turn(piece, move_count):
                    # Select the piece
                    selected_piece = piece
                    selected_square = clicked_square
                    # Highlight the selected square with a different color
                    highlight_square(screen, selected_square, cellSize,highlight_color=(255, 0, 0))
                    highlight_valid_moves(chessboard,screen, selected_piece, selected_square, cellSize)
                    selecting_piece = False  # Move to the state of selecting the destination square
                else:
                    # If no piece is selected, do nothing
                    pass
            elif not selecting_piece:
                    # If the player is currently selecting a destination square, this is the destination square
                    destination_square = clicked_square
                    if is_valid_move(chessboard, selected_square, destination_square, selected_piece,en_passant_square):
                        if is_valid_castling(chessboard, selected_square, destination_square, selected_piece):
                            # Perform castling
                            perform_castling(chessboard, selected_square, destination_square, selected_piece,move_count)
                        #check for enpassant
                        if is_valid_en_passant(chessboard, selected_square, destination_square, selected_piece, en_passant_square):
                            perform_en_passant(chessboard, selected_square, destination_square, selected_piece, en_passant_square)
                        if selected_piece[1] == 'P':
                            valid_move = is_valid_pawn_move(chessboard, selected_square, destination_square, selected_piece,en_passant_square)
                            if valid_move:
                                # Check for en passant and update the en_passant_square variable
                                if abs(selected_square[1] - destination_square[1]) == 2:
                                    en_passant_square = (destination_square[0], (selected_square[1] + destination_square[1]) // 2)
                                else:
                                    en_passant_square = None
                        # Check if the current move promotes a pawn
                        if (
                            selected_piece[1] == 'P' and
                            ((selected_piece[0] == 'w' and destination_square[1] == 0) or
                            (selected_piece[0] == 'b' and destination_square[1] == 7))
                        ):
                            # Perform pawn promotion
                            promoted_piece = promote_pawn(screen, cellSize, width, height, selected_piece[0])
                            chessboard[destination_square[1]][destination_square[0]] = selected_piece[0] + promoted_piece[0]
                        
                        else:
                            # Update the board state with the new move
                            chessboard[destination_square[1]][destination_square[0]] = selected_piece

                        chessboard[selected_square[1]][selected_square[0]] = None
                        move_count += 1  # Increment the move count
                        clear_highlights(screen, cellSize)  # Clear highlights after the move
                        # Check if the current player has any valid moves left
                        current_player = 'w' if move_count % 2 == 0 else 'b'
                        if not check_valid_moves(chessboard, current_player):
                            # Display game over message
                            font = pygame.font.Font(None, 36)
                            winner = 'Black' if current_player == 'w' else 'White'
                            text = font.render(f"Game Over. {winner} wins!", True, (255, 20, 30))
                            screen.blit(text, (width // 2 - 150, height // 2))
                            pygame.display.flip()
                            pygame.time.delay(2000)  # Display for 3 seconds
                            pygame.quit()
                            quit()

                    # Clear the selected piece and squares
                    selected_piece = None
                    selected_square = None
                    destination_square = None
                    selecting_piece = True  # Move back to the state of selecting a piece
                                        #update variables for castlling
                    print( chessboard[7][7],chessboard[7][0],chessboard[0][7],chessboard[0][0],chessboard[7][4],chessboard[0][4])
                    if  chessboard[7][7] != 'wR':
                        # White kingside rook square after a move
                            has_white_king_side_rook_moved = True
                    if  chessboard[7][0] != 'wR':
                        # White queenside rook square after a move
                        has_white_queen_side_rook_moved = True
                    if  chessboard[0][7] != 'bR':
                        # Black kingside rook square after a move
                        has_black_king_side_rook_moved = True
                    if  chessboard[0][0] != 'bR':
                        # Black queenside rook square after a move
                        has_black_queen_side_rook_moved = True
                    if chessboard[7][4] != 'wK':
                        # White king square after a move
                        has_white_king_moved = True
                    if chessboard[0][4] != 'bK':
                        # Black king square after a move
                        has_black_king_moved = True

                    # Draw the board with the updated piece positions
                    draw_pieces(screen, board, chessboard, IMAGES, cellSize)

    # # Draw the board with the updated piece positions
    # utils.draw_pieces(screen, board, chessboard, IMAGES, cellSize)

    # Update the display
    pygame.display.update()
    