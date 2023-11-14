import pygame
from pygame.locals import *
import main


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

# Main menu loop
def main_menu():
    pygame.init()

    # Set the display for the game
    width = 600
    height = 600
    size = (width, height)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Chess")

    # Load background image
    background_image = pygame.image.load("background.jpg")
    background_image = pygame.transform.scale(background_image, (width, height))

    # Set up fonts
    title_font = pygame.font.Font(None, 64)
    button_font = pygame.font.Font(None, 36)

    # Create buttons
    new_game_button = Button(200, 200, 200, 50, "New Game", (50, 205, 50), (0, 128, 0), main.playgame)
    quit_button = Button(200, 300, 200, 50, "Quit", (255, 69, 0), (178, 34, 34), pygame.quit)

    buttons = [new_game_button, quit_button]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in buttons:
                button.handle_event(event)

        # Draw background
        screen.blit(background_image, (0, 0))

        # Draw buttons
        for button in buttons:
            button.draw(screen, button_font)

        # Draw title
        title_text = title_font.render("Chess", True, (255, 255, 255))
        screen.blit(title_text, (width // 2 - 80, 50))

        pygame.display.flip()

    pygame.quit()
    quit()

# Run the main menu
main_menu()
