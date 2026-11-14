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

GENERATION_FRAMES = 3000
CHECKPOINT_RADIUS = 70

track_index = 0
current_track = training_tracks[track_index]

frame = 0
generation = 1
best_car_fitness = []
drawing = True

cars = []

for i in range(50):
    car = Car(current_track["start_x"], current_track["start_y"], current_track["start_angle"])
    cars.append(car)

def get_fitness(car):
    car_score = (car.completed, car.fitness, car.speed_score)

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

        # calculate fitness score
        for car in cars:
            car.fitness += min(car.progress(current_track["checkpoints"]), 1)

            if car.laps >= 1:
                car.completed += 1
                car.speed_score += 1 - car.lap_frames / GENERATION_FRAMES

        # if all tracks not finished yet -> start the new track and reset car positions
        if track_index < len(training_tracks) - 1:
            track_index += 1
            current_track = training_tracks[track_index]

            for car in cars:
                car.reset(current_track["start_x"], current_track["start_y"], current_track["start_angle"])
            frame = 0

        # if all tracks finished or one generation finished
        else:
            # cars sorted by fitness
            sorted_cars = sorted(cars, key=get_fitness, reverse=True)
            parents = sorted_cars[:10]      # find parents

            print("generation no: " +  str(generation))
            best = sorted_cars[0]
            print("completed:", best.completed, "| progress:", round(best.fitness, 2), "| speed:", round(best.speed_score, 2))

            generation += 1     # increase generation
            frame = 0           # reset frame
            cars = []           # delete old cars
            track_index = 0     # reset track index
            current_track = training_tracks[track_index]

            # save elite car and append to new list of cars
            elite_car = parents[0]
            elite = Car(current_track["start_x"], current_track["start_y"], current_track["start_angle"], elite_car.brain)
            cars.append(elite)

            best_car_fitness.append(elite_car.fitness)

            # create rest of the cars by crossover and mutation
            for i in range(49):
                parent1 = random.choice(parents)
                parent2 = random.choice(parents)

                new_brain = crossover(parent1.brain, parent2.brain)
                new_brain = mutate(new_brain)

                car = Car(current_track["start_x"], current_track["start_y"], current_track["start_angle"], new_brain)
                cars.append(car)

            with open("models/best_brain_v2.pkl", "wb") as file:
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

plt.plot(best_car_fitness)
plt.xlabel("generation")
plt.ylabel("best fitness")
plt.title("evolution progress")
plt.savefig("docs/fitness_latest.png")
plt.show()

pygame.quit()
