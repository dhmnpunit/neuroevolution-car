import pygame
import math
from brain import neuron

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
grass_mask = pygame.mask.from_threshold(track, (60, 150, 60, 255), (1, 1, 1, 255))

# car coordinates
START_X = 120
START_Y = 300 
x = START_X
y = START_Y

next_checkpoint = 0
score = 0
laps = 0

START_ANGLE = 90
angle = START_ANGLE
speed = 0
acceleration = 0.06


CHECKPOINTS = [(150, 130), (300, 95), (420, 190), (540, 95), (690, 130), (710, 300), (650, 480), (480, 520), (400, 435), (300, 515), (140, 460), (120, 300)]
CHECKPOINT_RADIUS = 70

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ###################
    ## LOGIC
    ###################

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
        angle += 2
    if keys[pygame.K_RIGHT]:
        angle -= 2

    # car rotation
    rotated_image = pygame.transform.rotate(car_image, angle)
    rotated_rect = rotated_image.get_rect(center=(x, y))

    car_mask = pygame.mask.from_surface(rotated_image)

    # crash detection and reset position
    if grass_mask.overlap(car_mask, (rotated_rect.x, rotated_rect.y)):
        x = START_X
        y = START_Y
        angle = START_ANGLE
        speed = 0
        next_checkpoint = 0
        score = 0
        laps = 0

    point = CHECKPOINTS[next_checkpoint]
    distance = math.dist((x, y), point)

    # checkpoint detection and score/laps count 
    if distance < CHECKPOINT_RADIUS:
        next_checkpoint += 1

        if next_checkpoint == len(CHECKPOINTS):
            laps += 1
            next_checkpoint = 0
            print("laps: " + str(laps))

        score += 1

        print(score)

    ###################
    ## DRAWING
    ###################

    # track 
    screen.blit(track, (0, 0))

    # car image
    screen.blit(rotated_image, rotated_rect)

    # checkpoints 
    for checkpoints in CHECKPOINTS:
        pygame.draw.circle(screen, (0, 150, 255), checkpoints, CHECKPOINT_RADIUS, 2)

    # yellow raycasting line    
    distances = []

    for offset in [90, 45, 0, -45, -90]:
        d = 0

        while d < 200:
            ray_x = x + d * math.cos(math.radians(angle + offset))
            ray_y = y - d * math.sin(math.radians(angle + offset))

            track_color = track.get_at((int(ray_x), int(ray_y)))
            if track_color == (60, 150, 60, 255):
                break
            d += 1

        distances.append(d/ 200)

        pygame.draw.line(screen, (255, 255, 0), (x, y), (ray_x, ray_y), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
