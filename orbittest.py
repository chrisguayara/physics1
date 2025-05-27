import pygame 
import sys
import math
import random
import time

class Camera:
    def __init__(self, pos, zoom=1.0):
        self.pos = pygame.Vector2(pos)
        self.zoom = zoom

    def load_screen(self, world_pos, screen_size):
        screen_center = pygame.Vector2(screen_size[0] // 2, screen_size[1] // 2)
        return (pygame.Vector2(world_pos) - self.pos) * self.zoom + screen_center

pygame.init()
clockMaster = pygame.time.Clock()
WIDTH, HEIGHT = 1280, 720
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("orbital")

bodies = []
count = 0

def create_body(name, rad, color, faraway):
    global count
    count += 1
    x = WIDTH // 2 
    y = HEIGHT // 2 - faraway
    newBody = {
        'name': name,
        'mass': 100,
        'pos': pygame.Vector2(x, y),
        'radius': rad,
        'angvel': 0.25 * abs(2 + (4 - count)),
        'color': color,
        'borderRad': faraway,
        'init_start': random.uniform(0, 2 * math.pi),
    }
    bodies.append(newBody)
    return newBody



mercury = create_body("mercury", 30, pygame.Color(255, 50, 0), 120)
earth = create_body("earth", 30, pygame.Color(51, 105, 255), 220)
mars = create_body("mars", 30, pygame.Color(155, 150, 0), 350)
jupiter = create_body("jupiter", 50, pygame.Color(251, 50, 55), 450)
moon = create_body("earthMoon", 18, pygame.Color(79, 79, 79), 100)
moon['angvel'] += 3



start_time = time.time()
camera = Camera((WIDTH // 2, HEIGHT // 2))

while True:
    delta = clockMaster.tick(120) / 1000
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            print(f"Key down: {pygame.key.name(e.key)}")
            if e.key == pygame.K_w:
                camera.zoom += 0.3
            elif e.key == pygame.K_s:
                camera.zoom -= 0.3

    largest_orbit = max(bods['borderRad'] for bods in bodies)
    minZoom = (HEIGHT/2)/largest_orbit
    camera.zoom = max(minZoom*.8, min(3, camera.zoom))

    for bods in bodies:
        totalTime = time.time() - start_time
        angle = bods['angvel'] * totalTime + bods['init_start']
        if bods != moon:
            bods['pos'].x = camera.pos.x + bods['borderRad'] * math.cos(angle)
            bods['pos'].y = camera.pos.y + bods['borderRad'] * math.sin(angle)
        else:
            bods['pos'].x = earth['pos'].x + bods['borderRad'] * math.cos(angle)
            bods['pos'].y = earth['pos'].y + bods['borderRad'] * math.sin(angle)

    window.fill((0, 0, 0))

    sun_pos = camera.load_screen(camera.pos, window.get_size())
    pygame.draw.circle(window, (255, 153, 0), sun_pos, int(34 * camera.zoom))

    for bods in bodies:
        screen_pos = camera.load_screen(bods['pos'], window.get_size())
        if bods != moon:
            pygame.draw.circle(window, (27, 27, 27), sun_pos, int(bods['borderRad'] * camera.zoom), 1)
        elif bods == moon:
            earth_screen = camera.load_screen(earth['pos'], window.get_size())
            pygame.draw.circle(window, (60, 60, 60), earth_screen, int(moon['borderRad'] * camera.zoom), 1)
        pygame.draw.circle(window, bods['color'], (int(screen_pos.x), int(screen_pos.y)), int(bods['radius'] * camera.zoom))

    pygame.display.flip()