# Imports
import pygame
import pygame.freetype
import subprocess

# Initialize pygame and extentions
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Set window dimensions
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Change window title properties
pygame.display.set_caption('PONG!!')
icon = pygame.image.load('PONG!!/Internal/WindowIcon.png')
pygame.display.set_icon(icon)

# Control framerate
clock = pygame.time.Clock()

# Class for handeling gameboard
class gamespace:
    def __init__(self):
        self.rect_width = 600
        self.rect_height = 300
        self.rect_x = (screen_width - self.rect_width) // 2  # Get X coordinate
        self.rect_y = (screen_height - self.rect_height) // 2  # Get Y coordinate

    def gameboard(self):
        background_img = pygame.image.load('PONG!!/Internal/Background.png')

        # Get the width and height of the background image
        bg_width, bg_height = background_img.get_size()

        # Blit the background image onto the screen
        screen.blit(background_img, (1280 - bg_width, 720 - bg_height))

        pygame.draw.rect(screen, (100, 100, 100), (self.rect_x - 4, self.rect_y - 4, self.rect_width + 8, self.rect_height + 8))  # Border
        pygame.draw.rect(screen, (255, 255, 255), (self.rect_x, self.rect_y, self.rect_width, self.rect_height))  # Interior

        # Load the image
        image = pygame.image.load("PONG!!/Internal/GameBoard.png")

        # Resize the image to fit the rectangle
        image = pygame.transform.scale(image, (self.rect_width, self.rect_height))

        # Blit the image onto the interior rectangle
        screen.blit(image, (self.rect_x, self.rect_y))
    
# Class for handeling score elements
class score:
    def __init__(self):
        self.rect_width = 250
        self.rect_height = 100
        self.rect_x = (screen_width - self.rect_width) // 2 # Get X coordinate
        self.rect_y = (screen_height - self.rect_width - 300) // 2 # Get Y coordinate

        self.player1_score = 0
        self.player2_score = 0
        self.score_increment = 1

        self.GAME_FONT = pygame.freetype.Font("PONG!!/Internal/PixelFont.ttf", 60)

    def draw_card(self):

        pygame.draw.rect(screen, (100, 100, 100), (self.rect_x - 4, self.rect_y - 4, self.rect_width + 8, self.rect_height + 8))    # Border
        pygame.draw.rect(screen, (255, 255, 255), (self.rect_x, self.rect_y, self.rect_width, self.rect_height))    # Interior

        box_img = pygame.image.load('PONG!!/Internal/ScoreCard.png')

        box_img = pygame.transform.scale(box_img, (self.rect_width, self.rect_height))

        screen.blit(box_img, (self.rect_x, self.rect_y))
    
        self.GAME_FONT.render_to(screen, (self.rect_x + 50, self.rect_y + 50),  str(self.player1_score), (255, 255, 255))
        self.GAME_FONT.render_to(screen, (self.rect_x + 175, self.rect_y + 50),  str(self.player2_score), (255, 255, 255))

# Class for handeling paddle elements
class Paddles:
    def __init__(self):
        # Define paddle dimensions
        self.paddle_width = 10
        self.paddle_height = 60

        # Initial positions of the paddles
        self.start_paddle1_x = 360
        self.start_paddle1_y = 330
        self.start_paddle2_x = self.start_paddle1_x + 550
        self.start_paddle2_y = 330

        # Define paddle speeds
        self.paddle_speed = 5

        # Create paddle rectangles
        self.paddle1_rect = pygame.Rect(self.start_paddle1_x, self.start_paddle1_y, self.paddle_width, self.paddle_height)
        self.paddle2_rect = pygame.Rect(self.start_paddle2_x, self.start_paddle2_y, self.paddle_width, self.paddle_height)

    # Update paddles
    def update(self):
        # Get the state of the keys
        keys = pygame.key.get_pressed()

        # Player 1 controls
        if keys[pygame.K_w]:
            self.start_paddle1_y -= self.paddle_speed
        if keys[pygame.K_s]:
            self.start_paddle1_y += self.paddle_speed

        # Player 2 controls
        if keys[pygame.K_UP]:
            self.start_paddle2_y -= self.paddle_speed
        if keys[pygame.K_DOWN]:
            self.start_paddle2_y += self.paddle_speed

        # Check if player 1's paddle collides with bottom/top of gameboard
        if self.start_paddle1_y <= gameboard.rect_y - 4 or self.start_paddle1_y >= gameboard.rect_y + gameboard.rect_height - self.paddle_height + 4:
            self.start_paddle1_y = self.paddle1_rect.y
            self.pointwin = pygame.mixer.music.load('PONG!!/Internal/pointwin.wav')
            self.pointwin = pygame.mixer.music.set_volume(1)
            self.pointwin = pygame.mixer.music.play()
        else:
            self.paddle_speed = 5

        # Check if player 2's paddle collides with bottom/top of gameboard
        if self.start_paddle2_y <= gameboard.rect_y - 4 or self.start_paddle2_y >= gameboard.rect_y + gameboard.rect_height - self.paddle_height + 4:
            self.start_paddle2_y = self.paddle2_rect.y
            self.pointwin = pygame.mixer.music.load('PONG!!/Internal/pointwin.wav')
            self.pointwin = pygame.mixer.music.set_volume(1)
            self.pointwin = pygame.mixer.music.play()
        else:
            self.paddle_speed = 5

        # Update the paddle rectangle
        self.paddle1_rect.y = self.start_paddle1_y
        self.paddle2_rect.y = self.start_paddle2_y

    # Draw the paddles
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.start_paddle1_x, self.start_paddle1_y, self.paddle_width, self.paddle_height))
        pygame.draw.rect(screen, (255, 255, 255), (self.start_paddle2_x, self.start_paddle2_y, self.paddle_width, self.paddle_height))
        
    def get_rect(self):
        # Return the bounding rectangle for the paddle
        return pygame.Rect(self.start_paddle1_x, self.start_paddle1_y, self.paddle_width, self.paddle_height)

# Class for handeling ball elements
class ball:
    def __init__(self, screen):
        # Define circle radius
        self.circle_radius = 7.5

        # Place circle in the center based on screen width and height
        self.circle_x = (screen.get_width() - self.circle_radius) // 2
        self.circle_y = (screen.get_height() - self.circle_radius) // 2

        # Define ball speed
        self.ball_speed_x = 6  # Horizontal speed
        self.ball_speed_y = 6  # Vertical speed

    def update_position(self):
        # Update ball position
        self.circle_x += self.ball_speed_x
        self.circle_y += self.ball_speed_y

        # Check if ball hits top or bottom of the game space
        if self.circle_y <= gameboard.rect_y - 4 or self.circle_y >= gameboard.rect_y + gameboard.rect_height + 4 - self.circle_radius * 2:
            self.ball_speed_y *= -1  # Reverse vertical direction
            self.hit = pygame.mixer.music.load('PONG!!/Internal/wallhit1.wav')
            self.hit = pygame.mixer.music.set_volume(1)
            self.hit = pygame.mixer.music.play()

        # Check if ball hits left side of gameboard
        if self.circle_x <= gameboard.rect_x - 4:
            self.ball_speed_x *= -1  # Reverse horizontal direction
            scorecard.player2_score += scorecard.score_increment
            self.pointwin = pygame.mixer.music.load('PONG!!/Internal/pointwin2.wav')
            self.pointwin = pygame.mixer.music.set_volume(1)
            self.pointwin = pygame.mixer.music.play()
            resetgame()

        # Check if ball hits right side of gameboard
        elif self.circle_x >= gameboard.rect_x + gameboard.rect_width + 4 - self.circle_radius * 2:
            self.ball_speed_x *= -1  # Reverse horizontal direction
            scorecard.player1_score += scorecard.score_increment
            self.pointwin = pygame.mixer.music.load('PONG!!/Internal/pointwin2.wav')
            self.pointwin = pygame.mixer.music.set_volume(1)
            self.pointwin = pygame.mixer.music.play()
            resetgame()
        
        # Check for ball-paddle collision
        if paddles.paddle1_rect.colliderect(self.get_rect()) or paddles.paddle2_rect.colliderect(self.get_rect()):
            self.ball_speed_x *= -1  # Reverse horizontal direction
            self.pointwin = pygame.mixer.music.load('PONG!!/Internal/pointwin.wav')
            self.pointwin = pygame.mixer.music.set_volume(1)
            self.pointwin = pygame.mixer.music.play()

    # Draw the ball
    def draw_ball(self, screen):
        pygame.draw.circle(screen, "grey", [self.circle_x, self.circle_y], self.circle_radius, 0)

    # Return the bounding rectangle for the ball
    def get_rect(self):
        return pygame.Rect(self.circle_x - self.circle_radius, self.circle_y - self.circle_radius, self.circle_radius * 2, self.circle_radius * 2)
    
# Create gameboard instance
gameboard = gamespace()

# Create scorecard instance
scorecard = score()

# Create paddles instance
paddles = Paddles()

# Create ball instance
ball = ball(screen)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update paddles
    paddles.update()

    # Update ball position
    ball.update_position()

    # Draw the gameboard
    gameboard.gameboard()

    # Draw the score card
    scorecard.draw_card()

    # Draw the paddles
    paddles.draw(screen)

    # Draw the ball
    ball.draw_ball(screen)


    # Reset the position of all objects when point is won
    def resetgame():
        paddles.start_paddle1_y = 330
        paddles.start_paddle2_y = 330

        # Place circle in the center based on screen width and height
        ball.circle_x = (screen.get_width() - ball.circle_radius) // 2
        ball.circle_y = (screen.get_height() - ball.circle_radius) // 2

    GAME_FONT = pygame.freetype.Font("PONG!!/Internal/PixelFont.ttf", 100)

    # Stop the game when a score goes over 5
    if scorecard.player1_score > 4:
        GAME_FONT.render_to(screen, (screen.get_width() // 2, screen.get_height() // 2),  "Player 2 wins", (255, 255, 255))
        pointwin1 = pygame.mixer.music.load('PONG!!/Internal/gameend.wav')
        pointwin1 = pygame.mixer.music.set_volume(1)
        pointwin1 = pygame.mixer.music.play()
        subprocess.run(['python', 'PONG!!/TitleScreen.py'])
        running = False
        #pygame.time.wait(3000)
        
    elif scorecard.player2_score > 4:
        GAME_FONT.render_to(screen, (screen.get_width() // 2, screen.get_height() // 2),  "Player 2 wins", (255, 255, 255))
        pointwin1 = pygame.mixer.music.load('PONG!!/Internal/gameend.wav')
        pointwin1 = pygame.mixer.music.set_volume(1)
        pointwin1 = pygame.mixer.music.play()
        subprocess.run(['python', 'PONG!!/TitleScreen.py'])
        running = False
        #pygame.time.wait(3000)

    # Flip the display to put your work on the screen
    pygame.display.flip()

    # Control framerate
    clock.tick(60)


# Quit Pygame
pygame.quit()
