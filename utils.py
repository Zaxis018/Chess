import pygame

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
