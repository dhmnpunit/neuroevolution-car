import math
from brain import create_brain, think

ACCELERATION = 0.06

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

    def drive(self):
        output = think(self.brain, self.distances)
        steer = output[0]
        gas = output[1]

        self.speed += gas * ACCELERATION
        self.angle -= steer * 2

        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))

        self.speed *= 0.98    