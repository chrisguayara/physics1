from pygame import *
import sys
import numpy as np
import math
import random
import copy




init()
mixer.init()
mixer.set_num_channels(64)
WIDTH, HEIGHT = 1600, 1000
center = [WIDTH//2, HEIGHT//2]
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Cwaft")
BLACK = (0, 0, 0)
GRAVITY = 0.3
ballCount = 25

clockMaster = time.Clock()

border_radius = 350
border_outline_w = 5

#ball params
ball_radius = 20
ball_outline_w = 4
ball_pos = center.copy()
ball_color = Color(255,255,255)


GRAVITY = 0.25
ball_velocity = [4, -9.8]
ball_acceleration = [0, GRAVITY]
balls = []

def create_ball():
    angle = random.uniform(0, 2*math.pi)
    radius = random.uniform(0, 330)
    x = WIDTH//2 + radius * math.cos(angle)
    y = HEIGHT//2 + radius * math.sin(angle)

    new_ball = {
        'pos' : [x, y],
        'velocity' : [random.choice([2, 1 , 0, -1, -2]), -5],
        'radius' : 20,
        'acceleration': [0, GRAVITY],
        'color' : random.randint(0, 360),
        'spawned' : False
    }
    balls.append(new_ball)
    balls.append(new_ball)

    return new_ball
create_ball()
ball_bouncing = False
balls[0]['radius'] = 10


#Times for creating new song points, in milliseconds
times = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
time_index = 0
tone_index = 0
tone_direction = 1
tones = [
    mixer.Sound("pop1.wav"),
    mixer.Sound("pop2.wav"),
    mixer.Sound("pop2.wav")
]
count = 0


while True:
    delta = clockMaster.tick(120)/1000
    for e in event.get():
        if e.type == QUIT:
            quit()
            sys.exit()
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                ball_bouncing = True
    if ball_bouncing:
        mainBall = balls[0]
        for ball in balls:
            ball['velocity'][1] += ball['acceleration'][1]
            ball['velocity'][0] += ball['acceleration'][0]
            ball['pos'][0] += ball['velocity'][0]
            ball['pos'][1] += ball['velocity'][1]

            dx = ball['pos'][0] - center[0]
            dy = ball['pos'][1] - center[1]
            distance_from_center = math.sqrt(dx**2+ dy**2)

            
            if distance_from_center >= border_radius - ball['radius']:
                
                normal = [dx/distance_from_center, dy/distance_from_center]
                dot_product = ball['velocity'][0] * normal[0] + ball['velocity'][1] * normal[1]
                reflection = [ball['velocity'][0] - 2 * dot_product * normal[0], ball['velocity'][1] -2 * dot_product * normal[1]]
                ball['velocity'] = [reflection[0], reflection[1]]
                ball['pos'][0] = center[0] + (border_radius - ball['radius']) * normal[0]
                ball['pos'][1] = center[1] + (border_radius - ball['radius']) * normal[1]
                channel = mixer.find_channel()
                
                
                tones[random.randint(0,2)].play()

                if not ball['spawned'] :
                    count += 1
                    balls.append(create_ball())
                    ball['spawned'] = True
                
               
                
                

            
            # for i in range(count): 
            #             create_ball()
            mainDx =mainBall['pos'][0] - ball['pos'][0]  
            mainDy = mainBall['pos'][1] - ball['pos'][1]  
            d_from_main = math.sqrt(mainDx**2 + mainDy**2)
            if ball != mainBall and (d_from_main <= mainBall['radius'] + ball['radius']):
                
                normal = [-mainDx/d_from_main, -mainDy/d_from_main]
                dot_product = ball['velocity'][0] * normal[0] + ball['velocity'][1] * normal[1]
                reflection = [ball['velocity'][0] - 2 * dot_product * normal[0], ball['velocity'][1] -2 * dot_product * normal[1]]
                ball['velocity'] = [reflection[0], reflection[1]]

                ball['pos'][0] = mainBall['pos'][0] + (mainBall['radius'] + ball['radius']) * normal[0]
                ball['pos'][1] = mainBall['pos'][1] + (mainBall['radius'] + ball['radius']) * normal[1]

                mainBall['velocity'] = [reflection[0]//4, reflection[1]//4]

                channel = mixer.find_channel()
                
                tones[random.randint(0,2)].play()

            
            
            # distance_from_Main = 
    

    window.fill(BLACK)

    draw.circle(window, (255, 255, 255), (center[0], center[1]), border_radius + border_outline_w)
    draw.circle(window, (0,0,0), (center[0], center[1]), border_radius)
    

   
    for ball in balls:
        ball_color.hsva = (ball['color'], 100, 40, 100)
        draw.circle(window, ball_color,(int(ball['pos'][0]), int(ball['pos'][1])), ball['radius'])
        ball_color.hsva = (ball['color'], 100, 90, 100)
        draw.circle(window, ball_color,(int(ball['pos'][0]), int(ball['pos'][1])), ball['radius'] - 4)

    
    display.flip()
    