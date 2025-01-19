import pygame
import time
import math
from typing import List,Dict,Tuple,Set
import numpy as np
import random

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
    
    def vector(self):
        return np.array([self.x,self.y])

class Container:

    def __init__(self,width:float,height:float,surface:pygame.Surface):

        self.anchor:Pair = Pair(100,100)
        self.width = width
        self.height = height
        self.surface=surface

    def draw(self):
        pygame.draw.rect(self.surface,(0,0,255),(self.anchor.x,self.anchor.y,self.width,self.height))
    
class Particle:

    id = 0

    def __init__(self,pos:Pair,v:Pair,radius:float,surface:pygame.Surface,e=0.8):

        self.pos=pos
        self.v:Pair=v
        self.surface=surface
        self.radius=radius
        self.e=e
        self.border = 0.5
        self.id = Particle.id
        Particle.id += 1

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
            self.v.y = -self.e * self.v.y
            self.pos.y = pos.y - self.radius + height
        # print(f"{self.pos},({pos.x+width},{pos.y+height})")
        # print(f"{self.v.tuple()},{self.pos.tuple()},{t}")
        # print(f"{self.pos.tuple()}")

def distance(p1:Pair,p2:Pair):
    # Euclidena distance
    return math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)

def particle_collision(p1:Particle,p2:Particle,e:float):
    #Function takes two particles and assigns them new velocities after collision
    
    print(f"{p1.pos} v/s {p2.pos}")


    #Find centers of both particles
    c1 = p1.pos.vector()
    c2 = p2.pos.vector()
    
    #Vector along the line joining the two centers
    vec_N = c2 - c1
    #Unit vector along the line joining the two centers
    vec_u_N = vec_N / np.linalg.norm(vec_N)

    #Velocity of particles along the line joining the two centers
    v1N = np.dot(p1.v.vector(),vec_u_N)
    v2N = np.dot(p2.v.vector(),vec_u_N)

    #Using conservation of momentum and coefficient of restitution
    v1N_new = ((1+e)*v2N+(1-e)*v1N)/2
    v2N_new = ((1-e)*v2N+(1+e)*v1N)/2

    #Turning the new velocity components into vector along x and y
    vec_v1N_new = v1N_new*vec_u_N
    vec_v2N_new = v2N_new*vec_u_N

    #The tangential components remain the same
    #Find the tangential vector or vector perpendicular to the normal
    vec_u_T = np.array([vec_u_N[1],vec_u_N[0]*-1])
    #The tangential components are
    vec_v1T_new = np.dot(p1.v.vector(),vec_u_T) * vec_u_T
    vec_v2T_new = np.dot(p2.v.vector(),vec_u_T) * vec_u_T

    v1_new = vec_v1N_new + vec_v1T_new
    v2_new = vec_v2N_new + vec_v2T_new

    #Assign the new velocities
    p1.v = Pair(v1_new[0],v1_new[1])
    p2.v = Pair(v2_new[0],v2_new[1])

    #Set new positions so that they dont continue collisions and their veclocities dont oscillate
    # point of collision
    c_mid = (c1+c2)/2
    # Unit vector from point of collision to center of p1
    vec_u_p1 = (c1-c_mid)/np.linalg.norm(c1-c_mid)
    vec_u_p2 = (c2-c_mid)/np.linalg.norm(c2-c_mid)

    # New position
    new_p1 = c_mid + (p1.radius+0.5)*vec_u_p1
    new_p2 = c_mid + (p2.radius+0.5)*vec_u_p2

    # Set position to particles
    p1.pos = Pair(new_p1[0],new_p1[1])
    p2.pos = Pair(new_p2[0],new_p2[1])


    #Set the position so that they are both a bit apart
    #Find the distance they differ by
    #Half this distance is how much I need to move each particle away from each other, along the line
    # d = distance(p1.pos,p2.pos)*0.5
    print(f"{p1.v.x}=={p2.v.x}")
    print(f"{p1.pos.x}<->{p2.pos.x}")
    # theta1 = math.atan((p1.pos.y-p2.pos.y)/(p1.pos.x-p2.pos.x))
    # theta2 = theta1 + math.radians(180)
    # p1.pos = Pair(math.floor(p1.pos.x-d*math.cos(theta1)),math.floor(p1.pos.y-d*math.sin(theta1)))
    # p2.pos = Pair(math.floor(p2.pos.x+d*math.cos(theta2)),math.floor(p2.pos.y+d*math.sin(theta2)))

    print("Collision")

class SpatialMap:

    def __init__(self,grid_size:float,particles:Dict[int,Particle]):
        self.grid_size = grid_size
        self.map: Dict[Tuple[int],List[int]] = dict()
        self.particles = particles

        for particle in particles.values():
            self.add(particle)

    def hash(self,pos:Pair):
        return (int(math.floor(pos.x / self.grid_size)),int(math.floor(pos.y / self.grid_size)))

    def add(self,p:Particle):

        h = self.hash(p.pos)
        if h not in self.map.keys():
            self.map[h] = [p.id]
        else:
            self.map[h].append(p.id)

    def update(self,id:int,old_pos:Pair,new_pos:Pair):
        old_hash = Pair(self.hash(old_pos)[0],self.hash(old_pos)[1])
        new_hash = Pair(self.hash(new_pos)[0],self.hash(new_pos)[1])

        if old_hash.x == new_hash.x and old_hash.y == new_hash.y:
            return
        
        #Delete old hash
        self.map[old_hash].remove(id)

        #Add new hash
        self.add(id,new_pos)

    def collision(self):

        #Find hash
        for h in self.map.keys():

        #Go through all the particles within this grid
        #If there is a collision, generate the new velocities
        
            for i in self.map[h]:
                for j in self.map[h]:
                    if i==j:
                        continue
                    p1 = self.particles[i]
                    p2 = self.particles[j]

                    if ((p1.pos.x-p2.pos.x)**2+(p1.pos.y-p2.pos.y)**2) < (p1.radius+p2.radius)**2:
                        # print(f"{(p1.pos.x-p2.pos.x)**2+(p1.pos.y-p2.pos.y)**2} vs {(p1.radius+p2.radius)**2}")
                        particle_collision(p1,p2,p1.e)

    def __str__(self):

        s = ""
        for key,val in self.map.items():
            s += f"{key}:{val}\n"

        return s

if __name__ == "__main__":

    NUM_PARTICLES = 100

    # Initialize Pygame
    pygame.init()

    # Create a screen (window)
    screen = pygame.display.set_mode((800, 600))  # Width: 800, Height: 600
    # Create the container
    container = Container(200,100,screen)
    pygame.display.set_caption("My Pygame Window")

    #List of particles
    # plist = [Particle(Pair(150,150+20*i),Pair(0,0),5,screen) for i in range(NUM_PARTICLES)]
    # plist = [Particle(Pair(150,150),Pair(0,0),10,screen),Particle(Pair(155,170),Pair(0,0),5,screen)]
    #Random particles
    plist:List[Particle] = []
    for i in range(NUM_PARTICLES):
        pos = Pair(random.randrange(container.anchor.x,container.anchor.x+container.width),random.randrange(container.anchor.y,container.anchor.y+container.height))
        v = Pair(random.randrange(-10,10),random.randrange(-10,10))
        plist.append(Particle(pos,v,5,screen))
    #Hashmap to access by ID
    particles = {x.id:x for x in plist}

    #Spatial map
    spatial_map = SpatialMap(25,particles)
    print(spatial_map)

    # #Create particle
    # p = Particle(Pair(150,150),Pair(10,10),10,screen)
    
    time_stamp = time.time()

    #Hashmap containing the 

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

        for p in plist:
            old_pos = p.pos
            p.move(Pair(0,9.8),elapsed)
            new_pos = p.pos
            spatial_map.update(p.id,old_pos,new_pos)
            p.collide_with_boundary(container.anchor,container.height,container.width,elapsed)
            p.draw()
        spatial_map.collision()

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()