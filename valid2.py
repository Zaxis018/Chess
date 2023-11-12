import utils

def is_valid_move(chessboard, source, destination, piece, en_passant_square=None):
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
    if chessboard[dest_y][dest_x] is not None and chessboard[dest_y][dest_x][0] == piece[0]:
        return False

    # Check if the move is valid for the specific piece type
    if piece[1] == 'P':
        valid_move = is_valid_pawn_move(chessboard, source, destination, piece)
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

# def is_king_in_check(chessboard, color): #error
#     # Find the king's position
#     for y in range(8):
#         for x in range(8):
#             piece = chessboard[y][x]
#             if piece is not None and piece[0] == color and piece[1] == 'K':
#                 king_position = (x, y)
#                 break

#     # Check if any opponent's piece can attack the king
#     opponent_color = 'b' if color == 'w' else 'w'
#     for y in range(8):
#         for x in range(8):
#             piece = chessboard[y][x]
#             if piece is not None and piece[0] == opponent_color:
#                 opponent_move = is_valid_move(chessboard, (x, y), king_position, piece)
#                 if opponent_move:
#                     return True  # King is in check
                

def is_king_in_check(chessboard, color):
    # Initialize king_position
    king_position = None

    # Find the king's position
    for y in range(8):
        for x in range(8):
            piece = chessboard[y][x]
            if piece is not None and piece[0] == color and piece[1] == 'K':
                king_position = (x, y)
                
    #Check if the king is found
    if king_position is None:
        return False

    # Check if any opponent's piece can attack the king
    opponent_color = 'b' if color == 'w' else 'w'
    for y in range(8):
        for x in range(8):
            piece = chessboard[y][x]
            if piece is not None and piece[0] == opponent_color:
                opponent_move = is_valid_move(chessboard, (x, y), king_position, piece)
                if opponent_move:
                    return True  # King is in check

    return False



def is_valid_pawn_move(chessboard,source, destination, piece):
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

def is_valid_bishop_move(chessboard,source, destination):
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

def is_valid_queen_move(chessboard,source, destination):
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
                        if is_valid_move(chessboard, (x, y), destination, piece):
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