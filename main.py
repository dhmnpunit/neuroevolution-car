import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Self Driving Car AI")

clock = pygame.time.Clock()

# car coordinates
x = 375
y = 287.5

angle = 90
speed = 3

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        x += speed * math.cos(math.radians(angle))
        y -= speed * math.sin(math.radians(angle))

    screen.fill((255, 255, 255))

    # car represented by a rectangle
    pygame.draw.rect(screen, "red", [x, y, 50, 25], 0)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
