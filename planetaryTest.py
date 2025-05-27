import pygame 
import sys
import math
import random
import time

pygame.init()
clockMaster = pygame.time.Clock()
WIDTH, HEIGHT = 1280, 920
window = pygame.display.set_mode((WIDTH, HEIGHT))
center = [WIDTH//2, HEIGHT//2]
pygame.display.set_caption("planets")
bodies = []

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

class Camera:
    def __init__(self, pos, zoom=1.0):
        self.pos = pygame.Vector2(pos)
        self.zoom = zoom

    def load_screen(self, world_pos, screen_size):
        screen_center = pygame.Vector2(screen_size[0] // 2, screen_size[1] // 2)
        return (pygame.Vector2(world_pos) - self.pos) * self.zoom + screen_center
    
class Circle:
    def __init__(self, color):
        self.color = color
    def create_body(self):
        mass = 7.35 * pow(10, 22)
        x, y = WIDTH//2, HEIGHT//2
        radius = random.randint(15, 30)
        bod = {
            'pos' : [random.randint(0, WIDTH),random.randint(0, HEIGHT)],
            'radius' : radius,
            'vel' : [random.randint(30,300),random.randint(50,400)],
            'accel' : [0, 0],
            'mass' : mass
        }
        bodies.append(bod)

gravity = 6.6/430 * pow(10,-11)
count = 2
arr = [0] * count
for i in arr:
    arr[i] = Circle(white)
    arr[i].create_body()



start_time = time.time()
isPressed = False
while True:
    delta = clockMaster.tick(120) / 1000
    curr_time = time.time() - start_time
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if e.key == pygame.K_w:
                force = random.randint(20,100)
                isPressed = True

    window.fill((0,0,0))
    

    for i in range(len(bodies)):
        for j in range(i + 1):
            bods = bodies[i]
            bods2 = bodies[j]
            if bods2 != bods:
                bods['vel'][0] += bods['accel'][0]
                bods['vel'][1] += bods['accel'][1]


                dx = bods['pos'][0] - bods2['pos'][0]
                dy = bods['pos'][1] - bods2['pos'][1]
                distance = math.sqrt(dx**2 + dy**2)
                radiiTogether = bods['radius'] + bods2['radius']      
                direction = [dx/distance , dy/distance]

                gforce = gravity * bods['mass'] * bods['mass'] / (distance**2) 
                accel = gforce/bods['mass']
                bods['accel'][0] = accel * direction[0]
                bods['accel'][1] = accel * direction[1]


                if distance!= 0 and distance < radiiTogether:
                    

                    overlap = radiiTogether - distance
                    nx = dx/distance
                    ny = dy/distance

                    bods['vel'][0] *= -.95
                    bods['vel'][1] *= -.95
                    bods['pos'][0] += nx * (overlap / 2)
                    bods['pos'][1] += ny * (overlap / 2)
                    

                    bods2['vel'][0] *= -.95
                    bods2['vel'][1] *= -.95
                    bods2['pos'][0] -= nx * (overlap / 2)
                    bods2['pos'][1] -= ny * (overlap / 2)
                
                
                

                    
        



        if isPressed:
            if bods['vel'][1] > 0 :
                bods['vel'][1] += force
            else: bods['vel'][1] += -force
            isPressed = False
        bods['vel'][1] += 9.81 * delta
        bods['pos'][0] += bods['vel'][0]
        bods['pos'][1] += bods['vel'][1]
        
        
        if bods['pos'][1] + bods['radius'] > HEIGHT: 
            bods['pos'][1] = HEIGHT - bods['radius']
            bods['vel'][1] *= -.95
        elif bods['pos'][1] - bods['radius'] < 0:
            bods['vel'][1] *= -.95
            bods['pos'][1] = bods['radius']
            
        if bods['pos'][0] + bods['radius'] > WIDTH:
            bods['pos'][0] = WIDTH - bods['radius']
            bods['vel'][0] *= -.95
        elif bods['pos'][0] - bods['radius'] < 0:
            bods['pos'][0] = bods['radius']
            bods['vel'][0] *= -.95

    
    for bods in bodies:
        
        
        pygame.draw.circle(window, (white), (int(bods['pos'][0]), int(bods['pos'][1])), int(bods['radius']))

    
    pygame.display.flip()
    pygame.display.update()
    