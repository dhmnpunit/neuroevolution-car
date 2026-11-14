import math
import pygame
from brain import create_brain, think

ACCELERATION = 0.06
GRASS_COLOR = (60, 150, 60, 255)
RAY_OFFSETS = [90, 60, 30, 0 , -30, -60, -90]
RAY_LENGTH = 200
BIG_STEP = 4                # ray stride: about 5x faster rays; can overshoot by a few px only when a ray grazes a wall edge
NO_PROGRESS_LIMIT = 800     # frames without reaching a new gate before a car is stopped (catches circlers)

class Car:
    def __init__(self, start_x, start_y, start_angle, brain = None):

        if brain is None:
            brain = create_brain()

        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.angle = start_angle
        self.speed = 0
        self.brain = brain
        self.fitness = 0
        self.score = 0
        self.frames = 0
        self.next_checkpoint = 0
        self.laps = 0
        self.distances = [1, 1, 1, 1, 1, 1, 1]
        self.alive = True
        self.rotated_image = None
        self.rotated_rect = None
        self.frames_since_gate = 0

    def reset(self, start_x, start_y, start_angle):
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.angle = start_angle
        self.speed = 0
        self.score = 0
        self.frames = 0
        self.laps = 0
        self.next_checkpoint = 0
        self.alive = True
        self.distances = [1, 1, 1, 1, 1, 1, 1]
        self.rotated_image = None
        self.rotated_rect = None
        self.frames_since_gate = 0

    def drive(self):
        output = think(self.brain, self.distances + [self.speed/ 3])
        steer = output[0]
        gas = output[1]

        self.speed += gas * ACCELERATION
        self.angle -= steer * 2

        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))

        self.speed *= 0.98  
        self.frames += 1  

    def sense(self, track):

        self.distances = []
        self.ray_ends = []

        for offset in RAY_OFFSETS:

            # the ray's direction never changes while we walk along it, so work it out once
            ray_angle = math.radians(self.angle + offset)
            step_x = math.cos(ray_angle)
            step_y = -math.sin(ray_angle)

            # big steps: jump BIG_STEP pixels at a time until we land on grass or run out of range
            d = 0
            while d < RAY_LENGTH:
                if track.get_at((int(self.x + d * step_x), int(self.y + d * step_y))) == GRASS_COLOR:
                    break
                d += BIG_STEP

            # small steps: back up one big step, then walk 1 pixel at a time to the exact edge
            if d < RAY_LENGTH:
                d = max(d - BIG_STEP, 0)
                while d < RAY_LENGTH:
                    if track.get_at((int(self.x + d * step_x), int(self.y + d * step_y))) == GRASS_COLOR:
                        break
                    d += 1

            d = min(d, RAY_LENGTH)
            self.distances.append(d / RAY_LENGTH)
            self.ray_ends.append([self.x + d * step_x, self.y + d * step_y])

    def detect_crash(self, car_image, grass_mask):
        self.rotated_image = pygame.transform.rotate(car_image, self.angle)     # rotate the image based on the angle
        self.rotated_rect = self.rotated_image.get_rect(center = (self.x, self.y))      # make a rectangle out of the rotated image

        car_mask = pygame.mask.from_surface(self.rotated_image)     # make the mask from the rotated image

        if grass_mask.overlap(car_mask, (self.rotated_rect.x, self.rotated_rect.y)):        # checks if car mask overlaps grass mask
            self.alive = False

    def calculate_score(self, checkpoints, checkpoint_radius):

        point = checkpoints[self.next_checkpoint]
        distance = math.dist((self.x, self.y), point)

        if distance < checkpoint_radius:
            self.next_checkpoint += 1
            self.frames_since_gate = 0

            if self.next_checkpoint == len(checkpoints):
                self.laps += 1
                self.alive = False
                self.lap_frames = self.frames
                self.next_checkpoint = 0

            self.score += 1
        else:
            # a car that stops making progress (e.g. circling) can't raise its score, so stop simulating it
            self.frames_since_gate += 1
            if self.frames_since_gate > NO_PROGRESS_LIMIT:
                self.alive = False


    def progress(self, checkpoints):
        if self.laps >= 1:
            return 1

        next_gate = checkpoints[self.next_checkpoint]
        if self.next_checkpoint == 0:
            prev_gate = (self.start_x, self.start_y)
        else:
            prev_gate = checkpoints[self.next_checkpoint - 1]

        gap = math.dist(prev_gate, next_gate)
        left = math.dist((self.x, self.y), next_gate)

        fraction = 1 - (left / gap)
        fraction = max(0, min(fraction, 1))

        return (self.score + fraction) / len(checkpoints)