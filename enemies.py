from ursina import *
from enum import Enum
from directions import Directions


class Enemy(Entity):

    # Defines a list of possible Actions
    class Actions(Enum):
        NOTHING = 0
        FORWARD = 1
        BACKWARD = 2
        LEFT = 3
        RIGHT = 4

    def __init__(self, maze, model='cube', texture='./assets/zombie.png', **kwargs):
        super().__init__(**kwargs)
        textures = ['assets/robot', 'assets/robot2', 'assets/zombie']
        self.texture = textures[random.randrange(textures.__len__())]
        self.model = 'plane'
        self.scale = (0.5, 0.5, 0.5)
        self.rotation = (-60, 90, 0)

        # Enemy Variables
        self.speed = 1/20
        self.player_path = []
        self.action = self.Actions.NOTHING
        self.maze = maze
        self.grid_position = self.position

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

    def update(self):

        # region Choose an Action

        if (self.action == self.Actions.NOTHING):

            # Direction list
            directions = []

            # Find Directions to go
            if (self.maze.Walls[round(self.x)][round(self.z)][0] == None and self.x+1 < self.maze.size):
                directions.append(Directions.FORWARD)

            if (self.x != 0 and self.maze.Walls[round(self.x-1)][round(self.z)][0] == None):
                directions.append(Directions.BACKWARD)

            if (self.maze.Walls[round(self.x)][round(self.z)][1] == None and self.z+1 < self.maze.size):
                directions.append(Directions.LEFT)

            if (self.z != 0 and self.maze.Walls[round(self.x)][round(self.z-1)][1] == None):
                directions.append(Directions.RIGHT)

            # Randomly choose an action
            direction = directions[random.randrange(directions.__len__())]

            # Set the action
            if (direction == Directions.FORWARD):
                self.set_action(self.Actions.FORWARD, Vec3(self.x+1,self.y,self.z))
            elif (direction == Directions.BACKWARD):
                self.set_action(self.Actions.BACKWARD, Vec3(self.x-1,self.y,self.z))
            elif (direction == Directions.LEFT):
                self.set_action(self.Actions.LEFT, Vec3(self.x,self.y,self.z+1))
            else:
                self.set_action(self.Actions.RIGHT, Vec3(self.x,self.y,self.z-1))

        # endregion

        # region Movement

        # If moving forward
        if (self.action == self.Actions.FORWARD):
            if (self.x + self.speed >= self.destination.x):
                self.x = self.destination.x
                self.action = self.Actions.NOTHING
                self.grid_position += (1, 0, 0)
            else:
                self.x += self.speed

        # If moving backward
        elif (self.action == self.Actions.BACKWARD):
            if (self.x - self.speed <= self.destination.x):
                self.x = self.destination.x
                self.action = self.Actions.NOTHING
                self.grid_position -= (1, 0, 0)
            else:
                self.x -= self.speed

        # If moving left
        elif (self.action == self.Actions.LEFT):

            if (self.z + self.speed >= self.destination.z):
                self.z = self.destination.z
                self.action = self.Actions.NOTHING
                self.grid_position += (0, 0, 1)
            else:
                self.z += self.speed

        # If moving right
        elif (self.action == self.Actions.RIGHT):
            if (self.z - self.speed <= self.destination.z):
                self.z = self.destination.z
                self.action = self.Actions.NOTHING
                self.grid_position -= (0, 0, 1)
            else:
                self.z -= self.speed

        # endregion
