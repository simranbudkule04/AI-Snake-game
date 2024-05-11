import pygame
import sys
import os

# Define some colors
BLACK = (0, 0, 0)
DARK_GREEN=(10, 104, 71)
WHITE = (255, 255, 255)
BG_COLOR = (135, 169, 34)
GREEN = (17, 66, 50)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)  # Light Blue color

# Define button class
class Button:
    def __init__(self, text, color, rect, action):
        self.text = text
        self.color = color
        self.rect = rect
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Initialize Pygame
pygame.init()

# Set the width and height of the screen [width, height]
SCREEN_WIDTH = 650
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Snake Game Menu")

# Create buttons
button1 = Button("1 player", GREEN, pygame.Rect(150, 250, 300, 50), "snake-human.py")
button2 = Button("1 player vs AI", GREEN, pygame.Rect(150, 350, 300, 50), "snake-human-ai.py")
button3 = Button("AI", GREEN, pygame.Rect(150, 450, 300, 50), "snake_ai.py")

buttons = [button1, button2, button3]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in buttons:
                if button.is_clicked(pos):
                    # Execute the Python file associated with the button
                    os.system("python " + button.action)

    # Change background color
    screen.fill(BG_COLOR)

    # Draw heading text
    font = pygame.font.Font(None, 48)
    heading_text = font.render("SNAKE GAME", True, BLACK)
    heading_rect = heading_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(heading_text, heading_rect)

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
