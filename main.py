import pygame
import math
from brain import create_brain, think
from car import Car

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Self Driving Car AI")

clock = pygame.time.Clock()

# car image
car_image = pygame.image.load("assets/car_red.png").convert_alpha()
car_image = pygame.transform.rotate(car_image, -90)
car_image = pygame.transform.scale(car_image, (50, 25))

# track image and mask
track = pygame.image.load("assets/track1.png").convert()
grass_mask = pygame.mask.from_threshold(track, (60, 150, 60, 255), (1, 1, 1, 255))

# car coordinates
START_X = 120
START_Y = 300 
START_ANGLE = 90

# checkpoints
CHECKPOINTS = [(150, 130), (300, 95), (420, 190), (540, 95), (690, 130), (710, 300), (650, 480), (480, 520), (400, 435), (300, 515), (140, 460), (120, 300)]
CHECKPOINT_RADIUS = 70

car_a = Car(START_X, START_Y, START_ANGLE)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ###################
    ## LOGIC
    ###################

    if car_a.alive == True:
        car_a.sense(track)
        car_a.drive()
        car_a.detect_crash(car_image, grass_mask)
        car_a.calculate_score(CHECKPOINTS, CHECKPOINT_RADIUS)

    ###################
    ## DRAWING
    ###################

    # display track on screen
    screen.blit(track, (0, 0))

    # display car image on screen
    screen.blit(car_a.rotated_image, car_a.rotated_rect)

    # display checkpoints 
    for checkpoints in CHECKPOINTS:
        pygame.draw.circle(screen, (0, 150, 255), checkpoints, CHECKPOINT_RADIUS, 2)

    # display rays
    for end in car_a.ray_ends:
        pygame.draw.line(screen, (255, 255, 0), (car_a.x, car_a.y), (end[0], end[1]), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
