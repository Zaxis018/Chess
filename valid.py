
def is_valid_move(chessboard,source, destination, piece):
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


def is_valid_pawn_move(chessboard,source, destination, piece):
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

def is_valid_rook_move(chessboard,source, destination):
    source_x,source_y=source
    dest_x,dest_y=destination
    if source_x!=dest_x and source_y!=dest_y: #cant change both x and y at same time ie only straight
        return False
    return True  

def is_valid_knight_move(chessboard,source, destination):
    # Implementation for Knight move validation
    return True  # Replace with your implementation

def is_valid_bishop_move(chesboard,source, destination):
    # Implementation for Bishop move validation
    return True  # Replace with your implementation

def is_valid_queen_move(chessboard,source, destination):
    # Implementation for Queen move validation
    return True  # Replace with your implementation

def is_valid_king_move(chessboard,source, destination):
    # Implementation for King move validation
    return True  # Replace with your implementation

def is_players_turn(chessboard,piece, move_count):
    # Check if it's White's turn (even move count) and the piece is a white piece
    if move_count % 2 == 0 and piece[0] == 'w':
        return True
    # Check if it's Black's turn (odd move count) and the piece is a black piece
    elif move_count % 2 == 1 and piece[0] == 'b':
        return True
    else:
        return False
    