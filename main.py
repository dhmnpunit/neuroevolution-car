import pygame
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
GENERATION_FRAMES = 2000

frame = 0
generation = 1

# checkpoints
CHECKPOINTS = [(150, 130), (300, 95), (420, 190), (540, 95), (690, 130), (710, 300), (650, 480), (480, 520), (400, 435), (300, 515), (140, 460), (120, 300)]
CHECKPOINT_RADIUS = 70

cars = []

for i in range(50):
    car = Car(START_X, START_Y, START_ANGLE)
    cars.append(car)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ###################
    ## LOGIC
    ###################

    dead = 0
    scores = []
    frame += 1

    for car in cars:
        if car.alive == True:
            car.sense(track)
            car.drive()
            car.detect_crash(car_image, grass_mask)
            car.calculate_score(CHECKPOINTS, CHECKPOINT_RADIUS)

        if not car.alive:
            dead += 1

        scores.append(car.score)        

    if dead == len(cars) or frame >= GENERATION_FRAMES:
        print("generation no: " +  str(generation))
        print("best score: " + str(max(scores)))

        generation += 1
        frame = 0
        cars = []

        for i in range(50):
            car = Car(START_X, START_Y, START_ANGLE)
            cars.append(car)

    ###################
    ## DRAWING
    ###################

    # display track on screen
    screen.blit(track, (0, 0))

    # display checkpoints 
    for checkpoints in CHECKPOINTS:
        pygame.draw.circle(screen, (0, 150, 255), checkpoints, CHECKPOINT_RADIUS, 2)

    for car in cars:
        # display car image on screen
        if car.alive and car.rotated_image is not None:
            screen.blit(car.rotated_image, car.rotated_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
