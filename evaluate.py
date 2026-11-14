import pickle
import pygame
import json
import sys
from car import Car 


pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Self Driving Car AI")

clock = pygame.time.Clock()

# tracks 
tracks = json.load(open("assets/tracks/tracks.json"))

# car image
car_image = pygame.image.load("assets/car_red.png").convert_alpha()
car_image = pygame.transform.rotate(car_image, -90)
car_image = pygame.transform.scale(car_image, (50, 25))

# constants 
GENERATION_FRAMES = 3000
CHECKPOINT_RADIUS = 70

with open("models/best_brain_v2.pkl", "rb") as file:
    brain = pickle.load(file)

for t in tracks:

    frame = 0

    track = pygame.image.load(t["image"]).convert()
    grass_mask = pygame.mask.from_threshold(track, (60, 150, 60, 255), (1, 1, 1, 255))

    car = Car(t["start_x"], t["start_y"], t["start_angle"], brain)

    while car.alive and frame < GENERATION_FRAMES:

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         sys.exit()

        car.sense(track)
        car.drive()
        car.detect_crash(car_image, grass_mask)
        car.calculate_score(t["checkpoints"], CHECKPOINT_RADIUS)

        screen.blit(track, (0, 0))

        if car.alive and car.rotated_image is not None:
            screen.blit(car.rotated_image, car.rotated_rect)

        # pygame.display.flip()
        # clock.tick(60)
        frame += 1


    print("name: " + t["name"])
    print("set: " + t["set"])

    progress = car.score / len(t["checkpoints"])
    print("progress: " + str(round(progress, 2)))

    print("laps: " + str(car.laps))

    if car.laps >= 1:
        print("alive")
    else:
        print("dead")

    print("-----")


pygame.quit()