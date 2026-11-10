import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Self Driving Car AI")

clock = pygame.time.Clock()
car_image = pygame.image.load("assets/car_red.png").convert_alpha()
car_image = pygame.transform.rotate(car_image, -90)
car_image = pygame.transform.scale(car_image, (50, 25))

# car coordinates
x = 400
y = 300

angle = 90
speed = 0
acceleration = 0.1

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        speed += acceleration
    if keys[pygame.K_DOWN]:
        speed -= acceleration

    x += speed * math.cos(math.radians(angle))
    y -= speed * math.sin(math.radians(angle))

    speed *= 0.98

    if keys[pygame.K_LEFT]:
        angle += 3
    if keys[pygame.K_RIGHT]:
        angle -= 3


    screen.fill((255, 255, 255))

    rotated_image = pygame.transform.rotate(car_image, angle)
    rotated_rect = rotated_image.get_rect(center=(x, y))

    # car image
    screen.blit(rotated_image, rotated_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
