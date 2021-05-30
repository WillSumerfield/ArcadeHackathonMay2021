from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from enum import Enum
from ursina.shaders import lit_with_shadows_shader


class Player(FirstPersonController):

    # Defines a list of possible Actions
    class Actions(Enum):
        NOTHING = 0
        FORWARD = 1
        BACKWARD = 2
        LEFT = 3
        RIGHT = 4
        UP = 5
        DOWN = 6

    def __init__(self, maze, **kwargs):

        # region Entity Arguments

        super().__init__(**kwargs)
        self.model = 'sphere'
        self.color = color.yellow
        self.alpha = 1
        self.scale = (0.6, 0.6, 0.6)
        self.position = (0,0,0)
        self.origin_y = 0
        self.shader = lit_with_shadows_shader

        # endregion

        # Movement Related
        self.action = self.Actions.NOTHING
        self.speed = 1/15
        self.destination = Vec3(self.x,self.y,self.z)
        self.maze = maze
        self.maze.set_visible_layer(0)
        self.grid_position = self.position

        # Remove Cursor
        self.cursor.texture = None
        self.cursor.model = None

        #Misc
        self.gameover = False

    def set_action(self, action, destination):

        # Check if you're not current doing anything
        if (self.action == self.Actions.NOTHING):

            # region Check if a wall blocks your action

            if (self.maze.two_dimension):

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

            # If the game is 3D
            else:
                if (action == self.Actions.FORWARD):
                    if (self.maze.Walls[round(self.grid_position[0])][round(self.grid_position[1])][round(self.grid_position[2])][0] != None or self.x+1 == self.maze.size):
                        return

                elif (action == self.Actions.BACKWARD):
                    if (self.maze.Walls[round(self.grid_position[0]-1)][round(self.grid_position[1])][round(self.grid_position[2])][0] != None or self.x == 0):
                        return

                elif (action == self.Actions.LEFT):
                    if (self.maze.Walls[round(self.grid_position[0])][round(self.grid_position[1])][round(self.grid_position[2])][2] != None or self.z+1 == self.maze.size):
                        return

                elif (action == self.Actions.RIGHT):
                    if (self.maze.Walls[round(self.grid_position[0])][round(self.grid_position[1])][round(self.grid_position[2]-1)][2] != None or self.z == 0):
                        return

                elif (action == self.Actions.UP):
                    if (self.maze.Walls[round(self.grid_position[0])][round(self.grid_position[1])][round(self.grid_position[2])][1] != None or self.y+1 == self.maze.size):
                        return

                elif (action == self.Actions.DOWN):
                    if (self.maze.Walls[round(self.grid_position[0])][round(self.grid_position[1]-1)][round(self.grid_position[2])][1] != None or self.y == 0):
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
        elif (held_keys['space']):
            # Check for Ladder
            if (self.maze.ladders[round(self.grid_position[0])][round(self.grid_position[1])][round(self.grid_position[2])] != None):
                self.set_action(self.Actions.UP, Vec3(self.x,self.y+1,self.z))
        else:
            # Check for Missing Floor
            if (self.maze.Walls[round(self.grid_position[0])][round(self.grid_position[1]-1)][round(self.grid_position[2])][1] == None):
                self.set_action(self.Actions.DOWN, Vec3(self.x,self.y-1,self.z))
            else:
                self.set_action(self.Actions.NOTHING, Vec3(self.x,self.y,self.z))

    def update(self):

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

        # If moving up
        elif (self.action == self.Actions.UP):
            if (self.y + self.speed >= self.destination.y):
                self.y = self.destination.y
                self.action = self.Actions.NOTHING
                self.grid_position += (0, 1, 0)
            else:
                self.y += self.speed

        # If moving down
        elif (self.action == self.Actions.DOWN):
            if (self.y - self.speed <= self.destination.y):
                self.y = self.destination.y
                self.action = self.Actions.NOTHING
                self.grid_position -= (0, 1, 0)
            else:
                self.y -= self.speed

        # If not moving
        else:
            pass

        # endregion

        # region Check for Collisions

        # region Point Collision

        for i in range(self.maze.points.__len__()):
            pt = self.maze.points[i]
            if (self.position == pt.position):
                destroy(pt)
                del self.maze.points[i]
                self.maze.current_points += 1
                break

        # endregion

        # region Enemy Collisions

        # For all enemies...
        for enemy in self.maze.enemies:

            # Check if there was a collision
            if (self.grid_position == enemy.grid_position):
                self.gameover = True

        # endregion

        self.maze.set_visible_layer(round(self.grid_position[1]))
        # endregion

