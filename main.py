import pygame
import random
import json
import pickle
from car import Car
from brain import mutate, crossover
import matplotlib.pyplot as plt

pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Self Driving Car AI")

clock = pygame.time.Clock()

tracks = json.load(open("assets/tracks/tracks.json"))
training_tracks = []

for t in tracks:
    if t["set"] == "train":
        training_tracks.append(t)

# track image and mask
for t in training_tracks:
    t["surface"] = pygame.image.load(t["image"]).convert()
    t["grass_mask"] = pygame.mask.from_threshold(t["surface"], (60, 150, 60, 255), (1, 1, 1, 255))

# car image
car_image = pygame.image.load("assets/car_red.png").convert_alpha()
car_image = pygame.transform.rotate(car_image, -90)
car_image = pygame.transform.scale(car_image, (50, 25))

GENERATION_FRAMES = 2000
CHECKPOINT_RADIUS = 70

track_index = 0
current_track = training_tracks[track_index]

frame = 0
generation = 1
best_scores = []
drawing = True

cars = []

for i in range(50):
    car = Car(current_track["start_x"], current_track["start_y"], current_track["start_angle"])
    cars.append(car)

def get_score(car):
    car_score = car.score

    return car_score

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                drawing = not drawing

    ###################
    ## LOGIC
    ###################

    dead = 0
    scores = []
    frame += 1

    for car in cars:
        if car.alive == True:
            car.sense(current_track["surface"])
            car.drive()
            car.detect_crash(car_image, current_track["grass_mask"])
            car.calculate_score(current_track["checkpoints"], CHECKPOINT_RADIUS)

        if not car.alive:
            dead += 1

        scores.append(car.score)        

    if dead == len(cars) or frame >= GENERATION_FRAMES:
        print("generation no: " +  str(generation))
        print("best score: " + str(max(scores)))

        sorted_cars = sorted(cars, key=get_score, reverse=True)
        parents = sorted_cars[:10]

        generation += 1
        best_scores.append(max(scores))
        frame = 0
        cars = []       

        elite_car = parents[0]
        elite = Car(current_track["start_x"], current_track["start_y"], current_track["start_angle"], elite_car.brain)
        cars.append(elite)     

        for i in range(49):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)

            new_brain = crossover(parent1.brain, parent2.brain)
            new_brain = mutate(new_brain)

            car = Car(current_track["start_x"], current_track["start_y"], current_track["start_angle"], new_brain)
            cars.append(car)

        with open("best_brain.pkl", "wb") as file:
            pickle.dump(elite_car.brain, file)

    ###################
    ## DRAWING
    ###################

    if drawing:
        # display track on screen
        screen.blit(current_track["surface"], (0, 0))

        # display checkpoints 
        # for checkpoints in CHECKPOINTS:
        #     pygame.draw.circle(screen, (0, 150, 255), checkpoints, CHECKPOINT_RADIUS, 2)

        for car in cars:
            # display car image on screen
            if car.alive and car.rotated_image is not None:
                screen.blit(car.rotated_image, car.rotated_rect)

        pygame.display.flip()
        clock.tick(60)

plt.plot(best_scores)
plt.xlabel("generation")
plt.ylabel("best score")
plt.title("evolution progress")
# plt.savefig("fitness_mut0.01.png")
plt.show()

pygame.quit()
