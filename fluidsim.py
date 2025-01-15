import pygame
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



class Pair:

    def __init__(self,x,y):
        self.x=x
        self.y=y

    def tuple(self):
        return (self.x,self.y)
    
    def __str__(self):
        return f"({self.x},{self.y})"

    def round(self):
        return (int(self.x),int(self.y))

class Container:

    def __init__(self,width:float,height:float,surface:pygame.Surface):

        self.anchor:Pair = Pair(100,100)
        self.width = width
        self.height = height
        self.surface=surface

    def draw(self):
        pygame.draw.rect(self.surface,(0,0,255),(self.anchor.x,self.anchor.y,self.width,self.height))
    
class Particle:

    def __init__(self,pos:Pair,v:Pair,radius:float,surface:pygame.Surface,e=0.8):

        self.pos=pos
        self.v:Pair=v
        self.surface=surface
        self.radius=radius
        self.e=e
        self.border = 0.5

    def move(self,acc:Pair,delta_time:float):

        #Update position
        self.pos.x += self.v.x*delta_time
        self.pos.y += self.v.y*delta_time

        #Update velocity
        self.v.x += acc.x*delta_time
        self.v.y += acc.y*delta_time

    def draw(self):

        #Draw a circle of small radius
        pygame.draw.circle(self.surface,(0,255,0),self.pos.tuple(),self.radius)        

    def collide_with_boundary(self,pos:Pair,height,width,t):

        #Check if we hit boundary
        #If so, reverse the velocity
        #Reset position to boundary
        if self.pos.x - self.radius < pos.x:
            self.v.x = -self.e * self.v.x
            self.pos.x = pos.x + self.radius
        elif self.pos.x + self.radius > pos.x+width:
            self.v.x = -self.e * self.v.x
            self.pos.x = pos.x - self.radius + width
        elif self.pos.y - self.radius < pos.y:
            self.v.y = -self.e * self.v.y
            self.pos.y = pos.y + self.radius
        elif self.pos.y + self.radius > pos.y+height:
            print("CASE")
            self.v.y = -self.e * self.v.y
            self.pos.y = pos.y - self.radius + height
        # print(f"{self.pos},({pos.x+width},{pos.y+height})")
        print(f"{self.v.tuple()},{self.pos.tuple()},{t}")

if __name__ == "__main__":



    # Initialize Pygame
    pygame.init()

    # Create a screen (window)
    screen = pygame.display.set_mode((800, 600))  # Width: 800, Height: 600
    # Create the container
    container = Container(200,100,screen)
    pygame.display.set_caption("My Pygame Window")

    #Create particle
    p = Particle(Pair(150,150),Pair(10,10),10,screen)
    
    time_stamp = time.time()

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit when the user closes the window
                running = False

        # Fill the screen with a color (e.g., white)
        screen.fill((255, 255, 255))

        # Draw a red rectangle (x, y, width, height)
        # pygame.draw.rect(screen, (255, 0, 0), (100, 100, 200, 150))
        container.draw()

        curr_time = time.time()
        elapsed = curr_time - time_stamp
        time_stamp = curr_time

        p.move(Pair(0,9.8),elapsed)
        p.collide_with_boundary(container.anchor,container.height,container.width,elapsed)
        p.draw()

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()