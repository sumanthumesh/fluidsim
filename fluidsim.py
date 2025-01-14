import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Pair:

    def __init__(self,x,y):
        self.x=x
        self.y=y

class Container:

    def __init__(self,width,height):

        self.anchor = (200,200)
        self.width = width
        self.height = height
    
class Particle:

    def __init__(self,posx,posy):

        self.x=posx
        self.y=posy

    def move(acceleration:Pair,delta_time:):




if __name__ == "__main__":

    # Initialize Pygame
    pygame.init()

    # Create a screen (window)
    screen = pygame.display.set_mode((800, 600))  # Width: 800, Height: 600
    pygame.display.set_caption("My Pygame Window")

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit when the user closes the window
                running = False

        # Fill the screen with a color (e.g., white)
        screen.fill((255, 255, 255))

        # Draw a red rectangle (x, y, width, height)
        pygame.draw.rect(screen, (255, 0, 0), (100, 100, 200, 150))

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()