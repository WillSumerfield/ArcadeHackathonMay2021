from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from enum import Enum
import keyboard


class Player(FirstPersonController):

    # Defines a list of possible Actions
    class Actions(Enum):
        NOTHING = 0
        FORWARD = 1
        BACKWARD = 2
        LEFT = 3
        RIGHT = 4

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = 'sphere'
        self.color = color.yellow
        self.alpha = 1
        self.scale = (0.6, 0.6, 0.6)
        self.position = (10,0,10)
        self.origin_y = 0
        self.action = self.Actions.NOTHING
        self.speed = 1/15
        self.destination = Vec3(self.x,self.y,self.z)

        # Remove Cursor
        self.cursor.texture = None
        self.cursor.model = None

    def set_action(self, action, destination):
        if (self.action == self.Actions.NOTHING):
            self.action = action
            self.destination = destination

    def input(self, key):

        if (held_keys['w']):
            self.set_action(self.Actions.FORWARD, Vec3(self.x+1,self.y,self.z))
        elif (held_keys['s']):
            self.set_action(self.Actions.BACKWARD, Vec3(self.x-1,self.y,self.z))
        elif (held_keys['a']):
            self.set_action(self.Actions.LEFT, Vec3(self.x,self.y,self.z+1))
        elif (held_keys['d']):
            self.set_action(self.Actions.RIGHT, Vec3(self.x,self.y,self.z-1))
        else:
            self.set_action(self.Actions.NOTHING, Vec3(self.x,self.y,self.z))

    def update(self):

        # If moving forward
        if (self.action == self.Actions.FORWARD):
            if (self.x + self.speed >= self.destination.x):
                self.x = self.destination.x
                self.action = self.Actions.NOTHING
            else:
                self.x += self.speed

        # If moving backward
        elif (self.action == self.Actions.BACKWARD):
            if (self.x - self.speed <= self.destination.x):
                self.x = self.destination.x
                self.action = self.Actions.NOTHING
            else:
                self.x -= self.speed

        # If moving left
        elif (self.action == self.Actions.LEFT):
            if (self.z + self.speed >= self.destination.z):
                self.z = self.destination.z
                self.action = self.Actions.NOTHING
            else:
                self.z += self.speed

        # If moving right
        elif (self.action == self.Actions.RIGHT):
            if (self.z - self.speed <= self.destination.z):
                self.z = self.destination.z
                self.action = self.Actions.NOTHING
            else:
                self.z -= self.speed



