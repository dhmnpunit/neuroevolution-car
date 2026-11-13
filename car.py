import math
import pygame
from brain import create_brain, think

ACCELERATION = 0.06
GRASS_COLOR = (60, 150, 60, 255)
RAY_LENGTH = 200
START_X = 120
START_Y = 300 
START_ANGLE = 90

class Car:
    def __init__(self, x, y, angle):

        brain = create_brain()

        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 0
        self.brain = brain
        self.score = 0
        self.next_checkpoint = 0
        self.laps = 0
        self.distances = [1, 1, 1, 1, 1]
        self.alive = True

    def drive(self):
        output = think(self.brain, self.distances)
        steer = output[0]
        gas = output[1]

        self.speed += gas * ACCELERATION
        self.angle -= steer * 2

        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))

        self.speed *= 0.98    

    def sense(self, track):

        self.distances = []
        self.ray_ends = []

        for offset in [90, 45, 0, -45, -90]:

            d = 0
    
            while d < RAY_LENGTH:
                ray_x = self.x + d * math.cos(math.radians(self.angle + offset))
                ray_y = self.y - d * math.sin(math.radians(self.angle + offset))
    
                track_color = track.get_at((int(ray_x), int(ray_y)))
                if track_color == GRASS_COLOR:
                    break
                d += 1
    
            self.distances.append(d/ 200)
            self.ray_ends.append([ray_x, ray_y])

    def detect_crash(self, car_image, grass_mask):
        self.rotated_image = pygame.transform.rotate(car_image, self.angle)     # rotate the image based on the angle
        self.rotated_rect = self.rotated_image.get_rect(center = (self.x, self.y))      # make a rectangle out of the rotated image

        car_mask = pygame.mask.from_surface(self.rotated_image)     # make the mask from the rotated image

        if grass_mask.overlap(car_mask, (self.rotated_rect.x, self.rotated_rect.y)):        # checks if car mask overlaps grass mask
            self.alive = False

    