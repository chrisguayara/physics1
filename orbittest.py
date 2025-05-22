import pygame 
import numpy as np
import sys
import math
import random
import time

pygame.init()
clockMaster = pygame.time.Clock()
WIDTH, HEIGHT = 1920, 1080
window = pygame.display.set_mode((WIDTH, HEIGHT))
border_radius = 350
center = [WIDTH // 2, HEIGHT // 2]
pygame.display.set_caption("Key")
bg_radius = 500

bodies = []
count = 0
def create_body(name, rad, color, faraway):
    global count
    count += 1
    x = WIDTH // 2 
    y = HEIGHT // 2 - faraway
    newBody = {
        'name' : name,
        'mass': 100,
        'pos': [x, y],
        'radius': rad,
        'angvel': .25*(abs(5 + (4 - count) )),
        'color': color,
        'borderRad' : faraway,
        'isChecked' : False,
        'init_start' : random.randint(0, 10)
    }
    newBody['tangSpeed'] = newBody['radius'] * newBody['angvel']
    newBody['cen_accel'] = newBody['tangSpeed']**2 / newBody['radius']
    bodies.append(newBody)
    return newBody


mercury = create_body("mercury", 30, pygame.Color(255, 200, 0), 150)
earth = create_body("earth", 50, pygame.Color(51,102,255), 250)
mars = create_body('mars', 53, pygame.Color(155,255,0), 350)
jupiter = create_body("jupiter", 100, pygame.Color(251,102,55), 500 )

start_time = time.time()



while True:
    delta = clockMaster.tick(120) / 1000
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit()
            sys.exit()
    
    
    #tang. vector logic
    for bods in bodies:
        randomness = random.randint(0,150)
        
            
        

        distx = center[0] - bods['pos'][0] 
        disty = center[1] - bods['pos'][1] 
        totalDist = math.sqrt(distx**2 + disty**2)

        nx = distx / totalDist 
        ny = disty / totalDist

        velx = -ny
        vely = nx
        

        totalTime = time.time() - start_time
        angle = bods['angvel'] * totalTime + bods['init_start']

        bods['pos'][0] = center[0] + bods['borderRad'] * math.cos(angle)
        bods['pos'][1] = center[1] + bods['borderRad'] * math.sin(angle)

        if randomness == 0:
            bods['borderRad'] += random.randint(-1, 1)
            bods['borderRad'] += random.randint(-1, 1)

    window.fill((0, 0, 0))
    pygame.draw.circle(window, (255, 153, 0), (center[0], center[1]), 75)
    for bods in bodies:

        pygame.draw.circle(window, bods['color'], (int(bods['pos'][0]), int(bods['pos'][1])), bods['radius'])
        
    pygame.display.flip()
