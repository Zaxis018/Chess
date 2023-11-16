import pygame
import valid

def get_square(event, cellSize, x_pos, y_pos):
    if event.button == 1:  # Left mouse button
        x = x_pos
        y = y_pos
        print(f"Left click at ({x}, {y})")
        # Logic to find out which square is the mouse clicked on
        clicked_square = (int(x // cellSize), int(y // cellSize))
        print(clicked_square)
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
            if valid.is_valid_move(chessboard,selected_square, destination_square, selected_piece):
                highlight_square(screen, destination_square, cellSize, highlight_color=(0, 255, 0))

def clear_highlights(screen, cellSize):
    for row in range(8):
        for col in range(8):
            square = (col, row)
            highlight_square(screen, square, cellSize, highlight_color=(255, 255, 255))  # Use the background color to "clear" the highlight


def promote_pawn(screen, cellSize, width, height, player_color):
    font = pygame.font.Font(None, 36)
    text = font.render("Choose piece", True, (255, 0, 0))
    screen.blit(text, (width // 3 +50, height //3 - 50))
    pygame.display.flip()

    promotion_options = ['Queen', 'Rook', 'Bishop', 'Night']
    option_rects = []

    piece_images = {
        'Queen': pygame.transform.scale(pygame.image.load(f'images/{player_color}Q.png'), (75, 75)),
        'Rook': pygame.transform.scale(pygame.image.load(f'images/{player_color}R.png'), (80, 80)),
        'Bishop': pygame.transform.scale(pygame.image.load(f'images/{player_color}B.png'), (80, 80)),
        'Night': pygame.transform.scale(pygame.image.load(f'images/{player_color}N.png'), (80, 80)),
    }

    for i, option in enumerate(promotion_options):
        rect = pygame.Rect(width // 3 - 50 + i * 100, height // 3, 100, 100)
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



