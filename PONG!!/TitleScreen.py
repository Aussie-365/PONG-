import pygame
import pygame.freetype
import subprocess

# Initialize pygame
pygame.init()

# Set window dimensions
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Load fonts
GAME_FONT = pygame.freetype.Font("PONG!!/Internal/PixelFont.ttf", 100)
BUTTON_FONT = pygame.freetype.Font("PONG!!/Internal/PixelFont.ttf", 40)

# Load the background image
background_img = pygame.image.load('PONG!!/Internal/Background.png').convert_alpha()
bg_width, bg_height = background_img.get_size()
opacity = 3
background_img.set_alpha(opacity)

# Define button properties
button_width = 200
button_height = 70
button_x = (screen_width - button_width) // 2
button_y = 300
button_color = (100, 100, 100)
hover_color = (150, 150, 150)
clicked_color = (200, 200, 200)
button_text = "Start Game"

# Function to draw the button
def draw_button():
    pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
    BUTTON_FONT.render_to(screen, (button_x + 20, button_y + 20), button_text, (255, 255, 255))



running = True
button_clicked = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Check if the mouse click is within the button's area
                if button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[1] <= button_y + button_height:
                    button_clicked = True
                    if button_clicked:
                        pointwin = pygame.mixer.music.load('PONG!!/Internal/wallhit2.wav')
                        pointwin = pygame.mixer.music.set_volume(1)
                        pointwin = pygame.mixer.music.play()
                        pygame.time.wait(500)
                        subprocess.run(['python', 'PONG!!/PongGame.py'])
                        running = False
                    else:
                        pass

        elif event.type == pygame.MOUSEMOTION:
            # Change button color when hovered over
            if button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[1] <= button_y + button_height:
                button_color = hover_color
            else:
                button_color = clicked_color if button_clicked else (100, 100, 100)

    screen.blit(background_img, (1280 - bg_width, 720 - bg_height))
    GAME_FONT.render_to(screen, (button_x, 200),  "PONG!!", (255, 255, 255))
    draw_button()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
