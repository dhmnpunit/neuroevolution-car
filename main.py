import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Self Driving Car AI")

clock = pygame.time.Clock()

# car image
car_image = pygame.image.load("assets/car_red.png").convert_alpha()
car_image = pygame.transform.rotate(car_image, -90)
car_image = pygame.transform.scale(car_image, (50, 25))

# track image
track = pygame.image.load("assets/track1.png").convert()

# car coordinates
x = 120
y = 300

angle = 90
speed = 0
acceleration = 0.08

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # acceleration and deceleration
    if keys[pygame.K_UP]:
        speed += acceleration
    if keys[pygame.K_DOWN]:
        speed -= acceleration

    # movement
    x += speed * math.cos(math.radians(angle))
    y -= speed * math.sin(math.radians(angle))

    # friction
    speed *= 0.98

    # rotation
    if keys[pygame.K_LEFT]:
        angle += 3
    if keys[pygame.K_RIGHT]:
        angle -= 3

    # crash detection
    color = track.get_at((int(x), int(y)))
    if color == (60, 150, 60, 255):
        print("crash")

    # track 
    screen.blit(track, (0, 0))

    # car rotation
    rotated_image = pygame.transform.rotate(car_image, angle)
    rotated_rect = rotated_image.get_rect(center=(x, y))

    # car image
    screen.blit(rotated_image, rotated_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
