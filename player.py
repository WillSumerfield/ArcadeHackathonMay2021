from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from enum import Enum


class Player(FirstPersonController):

    # Defines a list of possible Actions
    class Actions(Enum):
        NOTHING = 0
        FORWARD = 1
        BACKWARD = 2
        LEFT = 3
        RIGHT = 4

    def __init__(self, maze, **kwargs):

        # region Entity Arguments

        super().__init__(**kwargs)
        self.model = 'sphere'
        self.color = color.yellow
        self.alpha = 1
        self.scale = (0.6, 0.6, 0.6)
        self.position = (10,0,10)
        self.origin_y = 0

        # endregion

        # Movement Related
        self.action = self.Actions.NOTHING
        self.speed = 1/15
        self.destination = Vec3(self.x,self.y,self.z)
        self.maze = maze

        # Remove Cursor
        self.cursor.texture = None
        self.cursor.model = None

    def set_action(self, action, destination):

        # Check if you're not current doing anything
        if (self.action == self.Actions.NOTHING):

            # region Check if a wall blocks your action

            if (action == self.Actions.FORWARD):
                if (self.maze.Walls[round(self.x)][round(self.z)][0] != None or self.x+1 == self.maze.size):
                    return

            elif (action == self.Actions.BACKWARD):
                if (self.x == 0 or self.maze.Walls[round(self.x-1)][round(self.z)][0] != None):
                    return

            elif (action == self.Actions.LEFT):
                if (self.maze.Walls[round(self.x)][round(self.z)][1] != None or self.z+1 == self.maze.size):
                    return

            elif (action == self.Actions.RIGHT):
                if (self.z == 0 or self.maze.Walls[round(self.x)][round(self.z-1)][1] != None):
                    return

            # endregion

            # If it is not headed into a wall
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



