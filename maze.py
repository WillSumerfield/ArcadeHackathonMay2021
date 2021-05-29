from ursina import *
from directions import Directions
import random


class MazeWall(Entity):

    def __init__(self, position, direction, **kwargs):
        super().__init__(
            parent=scene,
            model='cube',
            origin=(0, 0, 0),
            alpha=1
        )
        self.position = position

        # Set Wall Based on Direction
        if (direction == Directions.FORWARD or direction == Directions.BACKWARD):
            self.position = position + (0.5, 0, 0)
            self.scale = (0.1, 1, 1)
            self.texture = 'texture_wall'

        elif (direction == Directions.RIGHT or direction == Directions.LEFT):
            self.position = position + (0, 0, 0.5)
            self.scale = (1, 1, 0.1)
            self.texture = 'texture_wall'

        else:
            self.position = position + (0, -0.5, 0)
            self.scale = (1, 0.1, 1)
            self.color = color.black


class Maze:

    def __init__(self, size, twodimension=True):

        # Instance Variables
        self.size = size

        # region Maze 2D

        if (twodimension):

            # Create Walls Grid
            self.Walls = [[[None for _ in range(3)] for _ in range(size)] for _ in range(size)]

            # Create Barriers Grid (Walls that are always there)
            self.Barriers = [[None for _ in range(size)] for _ in range(4)]

            # Create the Main Walls
            for x in range(size):
                for z in range(size):
                    if (x != size-1):
                        self.Walls[x][z][0] = MazeWall(position=(x, 0, z), direction=Directions.FORWARD)
                    if (z != size-1):
                        self.Walls[x][z][1] = MazeWall(position=(x, 0, z), direction=Directions.RIGHT)

            # Create the floors
            for x in range(size):
                for z in range(size):
                    self.Walls[x][z][2] = MazeWall(position=(x, 0, z), direction=Directions.UP)

            # Create Barriers
            for i in range(size):
                self.Barriers[0][i] = MazeWall(position=(size-1, 0, i), direction=Directions.FORWARD)
                self.Barriers[1][i] = MazeWall(position=(-1, 0, i), direction=Directions.BACKWARD)
                self.Barriers[2][i] = MazeWall(position=(i, 0, -1), direction=Directions.LEFT)
                self.Barriers[3][i] = MazeWall(position=(i, 0, size-1), direction=Directions.RIGHT)

        # endregion

        # region Carve Maze

        # region Variables

        # The squares still open
        visited = [[False for _ in range(size)] for _ in range(size)]

        # A list containing spaces with adjacent open squares
        open_adjacent = []

        # The number of visited and total spaces
        visited_count = 0
        total = size * size

        # The current Position
        pos = [10, 10]

        # endregion

        while (visited_count < total):

            # Set the current space to not empty
            visited[pos[0]][pos[1]] = True
            visited_count += 1

            # The directions we can go
            directions = []

            # region Find the Available Directions

            # Can we move forward?
            if (pos[0]+1 < size and not visited[pos[0]+1][pos[1]]):
                directions.append(Directions.FORWARD)

            # Can we move backward?
            if (pos[0] != 0 and not visited[pos[0]-1][pos[1]]):
                directions.append(Directions.BACKWARD)

            # Can we move left?
            if (pos[1] < size and not visited[pos[0]][pos[1]+1]):
                directions.append(Directions.LEFT)

            # Can we move right?
            if (pos[1] != 0 and not visited[pos[0]][pos[1]-1]):
                directions.append(Directions.RIGHT)

            # endregion

            # region Randomly choose and go in an available Direction and break the wall
            if (directions.__len__() != 0):

                direction = directions[random.randrange(directions.__len__())]

                print(f"{direction}")

                # Change the pos and break the Wall
                if (direction == Directions.FORWARD):
                    destroy(self.Walls[pos[0]][pos[1]][0])
                    self.Walls[pos[0]][pos[1]][0] = None
                    pos[0] += 1

                elif (direction == Directions.BACKWARD):
                    destroy(self.Walls[pos[0]-1][pos[1]][0])
                    self.Walls[pos[0]-1][pos[1]][0] = None
                    pos[0] -= 1

                elif (direction == Directions.LEFT):
                    destroy(self.Walls[pos[0]][pos[1]][1])
                    self.Walls[pos[0]][pos[1]][1] = None
                    pos[1] += 1

                else:
                    destroy(self.Walls[pos[0]][pos[1]-1][1])
                    self.Walls[pos[0]][pos[1]-1][1] = None
                    pos[1] -= 1

            # endregion

            # region Otherwise, backtrack

            else:
                pass

            # endregion

        # endregion
