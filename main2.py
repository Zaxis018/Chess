import pygame
from pygame.locals import *
import utils
import valid

# Initialize Pygame
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
board.fill((220, 220, 255))  # white first

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
utils.draw_pieces(screen, board, chessboard, IMAGES, cellSize)

#print(chessboard)

def promote_pawn(screen, cellSize):
    font = pygame.font.Font(None, 36)
    text = font.render("Pawn Promotion", True, (255, 255, 255))
    screen.blit(text, (width // 2 - 150, height // 2 - 50))
    pygame.display.flip()

    promotion_options = ['Queen', 'Rook', 'Bishop', 'Night']  # You can customize the options
    option_rects = []

    for i, option in enumerate(promotion_options):
        rect = pygame.Rect(width // 2 - 50 + i * 100, height // 2, 100, 50)
        pygame.draw.rect(screen, (0, 0, 255), rect, 2)
        option_rects.append(rect)
        text = font.render(option, True, (0, 0, 255))
        screen.blit(text, (rect.x + 10, rect.y + 10))

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
                if piece is not None and utils.is_players_turn(piece, move_count):
                    # Select the piece
                    selected_piece = piece
                    selected_square = clicked_square
                    # Highlight the selected square with a different color
                    utils.highlight_square(screen, selected_square, cellSize,highlight_color=(255, 0, 0))
                    utils.highlight_valid_moves(chessboard,screen, selected_piece, selected_square, cellSize)
                    selecting_piece = False  # Move to the state of selecting the destination square
                else:
                    # If no piece is selected, do nothing
                    pass
            elif not selecting_piece: 
                # If the player is currently selecting a destination square, this is the destination square
                destination_square = clicked_square
                if valid.is_valid_move(chessboard, selected_square, destination_square, selected_piece):
                    # Check if the current move promotes a pawn
                    if (
                        selected_piece[1] == 'P' and
                        ((selected_piece[0] == 'w' and destination_square[1] == 0) or
                        (selected_piece[0] == 'b' and destination_square[1] == 7))
                    ):
                        # Perform pawn promotion
                        promoted_piece = promote_pawn(screen, cellSize)
                        chessboard[destination_square[1]][destination_square[0]] = selected_piece[0] + promoted_piece[0]
                    else:
                        # Update the board state with the new move
                        chessboard[destination_square[1]][destination_square[0]] = selected_piece

                    chessboard[selected_square[1]][selected_square[0]] = None
                    print(chessboard)
                    move_count += 1  # Increment the move count
                    utils.clear_highlights(screen, cellSize)  # Clear highlights after the move

                    # Check if the current player has any valid moves left
                    current_player = 'w' if move_count % 2 == 0 else 'b'
                    if not valid.check_valid_moves(chessboard, current_player):
                        # Display game over message
                        font = pygame.font.Font(None, 36)
                        winner = 'Black' if current_player == 'w' else 'White'
                        text = font.render(f"Game Over. {winner} wins!", True, (255, 0, 0))
                        screen.blit(text, (width // 2 - 150, height // 2))
                        pygame.display.flip()
                        pygame.time.delay(3000)  # Display for 3 seconds
                        pygame.quit()
                        quit()



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
    