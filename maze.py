from ursina import *
from ursina.shaders import lit_with_shadows_shader
from directions import Directions
from enemies import Enemy

# Randomize the Seed
random.seed()


# The tic-tacs picked up by Pacman
class Point(Entity):

    def __init__(self, **kwargs):
        super().__init__(
            model='sphere',
            color=color.white,
            scale=(0.1, 0.1, 0.1),
            origin_y=0,
            **kwargs)


class Ladder(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            parent=scene,
            model='cube',
            color=color.brown,
            scale=(0.1, 1, 0.1),
            alpha=1,
            **kwargs
        )


# The Walls which make the maze
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
            self.scale = (0.1, 1.05, 1.05)
            self.texture = 'texture_wall'

        elif (direction == Directions.RIGHT or direction == Directions.LEFT):
            self.position = position + (0, 0, 0.5)
            self.scale = (1.05, 1.05, 0.1)
            self.texture = 'texture_wall'

        else:
            self.position = position + (0, 0.5, 0)
            self.scale = (1.05, 0.1, 1.05)
            self.color = color.black


# The Maze object given to the app for characters to interact with
class Maze:

    def __init__(self, size, random_deletion=0.1, points_per_square=0.1, enemies_per_layer=2, two_dimension=True):

        # region Instance Variables

        self.size = size
        self.two_dimension = two_dimension

        # endregion

        # region Maze 2D

        if (two_dimension):

            # region Wall Creation

            # Create Walls Grid
            self.Walls = [[[None for _ in range(3)] for _ in range(size)] for _ in range(size)]

            # Create Barriers Grid (Walls that are always there)
            self.Barriers = [[None for _ in range(size)] for _ in range(4)]

            # Create the Main Walls
            for x in range(size):
                for z in range(size):
                    if (x != size - 1):
                        self.Walls[x][z][0] = MazeWall(position=(x, 0, z), direction=Directions.FORWARD)
                    if (z != size - 1):
                        self.Walls[x][z][1] = MazeWall(position=(x, 0, z), direction=Directions.RIGHT)

            # Create the floors
            for x in range(size):
                for z in range(size):
                    self.Walls[x][z][2] = MazeWall(position=(x, 0, z), direction=Directions.UP)

            # Create Barriers
            for i in range(size):
                self.Barriers[0][i] = MazeWall(position=(size - 1, 0, i), direction=Directions.FORWARD)
                self.Barriers[1][i] = MazeWall(position=(-1, 0, i), direction=Directions.BACKWARD)
                self.Barriers[2][i] = MazeWall(position=(i, 0, -1), direction=Directions.LEFT)
                self.Barriers[3][i] = MazeWall(position=(i, 0, size - 1), direction=Directions.RIGHT)

            # endregion

            # region Carve Maze

            # region Variables

            # The squares still open
            visited = [[False for _ in range(size)] for _ in range(size)]

            # A list containing spaces with adjacent open squares
            unvisitied_adjacent = []

            # The number of visited and total spaces
            visited_count = 0
            total = size * size

            # The current Position
            pos = [0, 0]

            # endregion

            # Carve out every space
            while (visited_count < total):

                # If we haven't visited here before, record that we have
                if (not visited[pos[0]][pos[1]]):
                    visited[pos[0]][pos[1]] = True
                    visited_count += 1

                # The directions we can go
                directions = []

                # region Find the Available Directions

                # Can we move forward?
                if (pos[0] + 1 < size and not visited[pos[0] + 1][pos[1]]):
                    directions.append(Directions.FORWARD)

                # Can we move backward?
                if (pos[0] != 0 and not visited[pos[0] - 1][pos[1]]):
                    directions.append(Directions.BACKWARD)

                # Can we move left?
                if (pos[1] + 1 < size and not visited[pos[0]][pos[1] + 1]):
                    directions.append(Directions.LEFT)

                # Can we move right?
                if (pos[1] != 0 and not visited[pos[0]][pos[1] - 1]):
                    directions.append(Directions.RIGHT)

                # endregion

                # region Randomly choose and go in an available Direction and break the wall
                if (directions.__len__() != 0):

                    # Randomly choose Direction
                    direction = directions[random.randrange(directions.__len__())]

                    # If there are more ways to go, remember this space
                    if (directions.__len__() > 1):
                        unvisitied_adjacent.append(pos.copy())

                    # Change the pos and break the Wall
                    if (direction == Directions.FORWARD):
                        destroy(self.Walls[pos[0]][pos[1]][0])
                        self.Walls[pos[0]][pos[1]][0] = None
                        pos[0] += 1

                    elif (direction == Directions.BACKWARD):
                        destroy(self.Walls[pos[0] - 1][pos[1]][0])
                        self.Walls[pos[0] - 1][pos[1]][0] = None
                        pos[0] -= 1

                    elif (direction == Directions.LEFT):
                        destroy(self.Walls[pos[0]][pos[1]][1])
                        self.Walls[pos[0]][pos[1]][1] = None
                        pos[1] += 1

                    else:
                        destroy(self.Walls[pos[0]][pos[1] - 1][1])
                        self.Walls[pos[0]][pos[1] - 1][1] = None
                        pos[1] -= 1

                # endregion

                # region Otherwise, backtrack

                else:
                    pos = unvisitied_adjacent.pop()

                # endregion

            # Remove some walls randomly
            for i in range(round(random_deletion * total)):
                # Get X, Z, and Direction
                wall_x = random.randrange(size)
                wall_z = random.randrange(size)
                wall_dir = random.randrange(2)

                # Check if Wall Exists
                if (self.Walls[wall_x][wall_z][wall_dir] != None):
                    destroy(self.Walls[wall_x][wall_z][wall_dir])
                    self.Walls[wall_x][wall_z][wall_dir] = None

            # endregion

            # region Point Creation

            # How many total points there are
            self.total_points = round(points_per_square * total)

            # How many points have been gotten
            self.current_points = 0

            # A list of all points
            self.points = []

            # Create a matrix of all possible point spots
            remaining_points = [(x, 0, z) for x in range(self.size) for z in range(self.size)]

            # Remove the starting position
            del remaining_points[0]

            # Create a point randomly for each pps
            for i in range(self.total_points):
                self.points.append(Point(position=remaining_points[random.randrange(remaining_points.__len__())]))

            # endregion

            # region Enemy Creation

            # A list of all enemies
            self.enemies = []

            # Create a matrix of all possible enemy spots
            remaining_spaces = [(x, 0, z) for x in range(self.size) for z in range(self.size)]

            # Remove the starting positions
            del remaining_spaces[0]

            # Create an enemy for each layer
            for i in range(enemies_per_layer):
                space = random.randrange(remaining_spaces.__len__())
                self.enemies.append(Enemy(self, position=remaining_spaces[space]))
                del remaining_spaces[space]

            # endregion

        # endregion

        # region Maze 3D

        total = size * size * size

        # region Wall Creation

        # Create Walls Grid
        self.Walls = [[[[None for _ in range(3)] for _ in range(size)] for _ in range(size)] for _ in range(self.size)]

        # Create Barriers Grid (Walls that are always there)
        self.Barriers_x = [[None for _ in range(2)] for _ in range(self.size * self.size)]
        self.Barriers_y = [[None for _ in range(2)] for _ in range(self.size * self.size)]
        self.Barriers_z = [[None for _ in range(2)] for _ in range(self.size * self.size)]

        # Create the Main Walls
        for x in range(size):
            for y in range(size):
                for z in range(size):
                    if (x != size - 1):
                        self.Walls[x][y][z][0] = MazeWall(position=(x, y, z), direction=Directions.FORWARD)
                    if (y != size - 1):
                        self.Walls[x][y][z][1] = MazeWall(position=(x, y, z), direction=Directions.UP)
                    if (z != size - 1):
                        self.Walls[x][y][z][2] = MazeWall(position=(x, y, z), direction=Directions.LEFT)

        # Create Barriers
        for y in range(self.size):
            for z in range(self.size):
                self.Barriers_x[(y * self.size) + z][0] = MazeWall(position=(-1, y, z), direction=Directions.FORWARD)
                self.Barriers_x[(y * self.size) + z][1] = MazeWall(position=(size - 1, y, z), direction=Directions.BACKWARD)

        for x in range(self.size):
            for z in range(self.size):
                self.Barriers_y[(x * self.size) + z][0] = MazeWall(position=(x, -1, z), direction=Directions.UP)
                self.Barriers_y[(x * self.size) + z][1] = None  # MazeWall(position=(x, size-1, z), direction=Directions.DOWN)

        for y in range(self.size):
            for x in range(self.size):
                self.Barriers_z[(y * self.size) + x][0] = MazeWall(position=(x, y, -1), direction=Directions.LEFT)
                self.Barriers_z[(y * self.size) + x][1] = MazeWall(position=(x, y, size - 1), direction=Directions.RIGHT)

        # endregion

        # region Carve Maze

        # region Variables

        # The squares still open
        visited = [[[False for _ in range(size)] for _ in range(size)] for _ in range(size)]

        # A list containing spaces with adjacent open squares
        unvisitied_adjacent = []

        # The number of visited and total spaces
        visited_count = 0

        # The current Position
        pos = [0, 0, 0]

        # endregion

        # Ladders Created
        self.ladders = [[[None for _ in range(size)] for _ in range(size)] for _ in range(size)]
        self.ladder_list = []

        # Carve out every space
        while (visited_count < total):

            # If we haven't visited here before, record that we have
            if (not visited[pos[0]][pos[1]][pos[2]]):
                visited[pos[0]][pos[1]][pos[2]] = True
                visited_count += 1

            # The directions we can go
            directions = []

            # region Find the Available Directions

            # Can we move forward?
            if (pos[0] + 1 < size and not visited[pos[0] + 1][pos[1]][pos[2]]):
                directions.append(Directions.FORWARD)

            # Can we move backward?
            if (pos[0] != 0 and not visited[pos[0] - 1][pos[1]][pos[2]]):
                directions.append(Directions.BACKWARD)

            # Can we move up?
            if (pos[1] + 1 < size and not visited[pos[0]][pos[1] + 1][pos[2]]):
                directions.append(Directions.UP)

            # Can we move down?
            if (pos[1] != 0 and not visited[pos[0]][pos[1] - 1][pos[2]]):
                directions.append(Directions.DOWN)

            # Can we move left?
            if (pos[2] + 1 < size and not visited[pos[0]][pos[1]][pos[2] + 1]):
                directions.append(Directions.LEFT)

            # Can we move right?
            if (pos[2] != 0 and not visited[pos[0]][pos[1]][pos[2] - 1]):
                directions.append(Directions.RIGHT)

            # endregion

            # region Randomly choose and go in an available Direction and break the wall

            if (directions.__len__() != 0):

                # Randomly choose Direction
                direction = directions[random.randrange(directions.__len__())]

                # If there are more ways to go, remember this space
                if (directions.__len__() > 1):
                    unvisitied_adjacent.append(pos.copy())

                # Change the pos and break the Wall
                if (direction == Directions.FORWARD):
                    destroy(self.Walls[pos[0]][pos[1]][pos[2]][0])
                    self.Walls[pos[0]][pos[1]][pos[2]][0] = None
                    pos[0] += 1

                elif (direction == Directions.BACKWARD):
                    destroy(self.Walls[pos[0] - 1][pos[1]][pos[2]][0])
                    self.Walls[pos[0] - 1][pos[1]][pos[2]][0] = None
                    pos[0] -= 1

                elif (direction == Directions.UP):
                    destroy(self.Walls[pos[0]][pos[1]][pos[2]][1])
                    self.Walls[pos[0]][pos[1]][pos[2]][1] = None
                    if (self.ladders[pos[0]][pos[1]][pos[2]] == None):
                        self.ladders[pos[0]][pos[1]][pos[2]] = Ladder(position=(pos[0], pos[1], pos[2]))
                        self.ladder_list.append(self.ladders[pos[0]][pos[1]][pos[2]])
                    pos[1] += 1

                elif (direction == Directions.DOWN):
                    destroy(self.Walls[pos[0]][pos[1] - 1][pos[2]][1])
                    self.Walls[pos[0]][pos[1] - 1][pos[2]][1] = None
                    pos[1] -= 1
                    if (self.ladders[pos[0]][pos[1]][pos[2]] == None):
                        self.ladders[pos[0]][pos[1]][pos[2]] = Ladder(position=(pos[0], pos[1], pos[2]))
                        self.ladder_list.append(self.ladders[pos[0]][pos[1]][pos[2]])

                elif (direction == Directions.LEFT):
                    destroy(self.Walls[pos[0]][pos[1]][pos[2]][2])
                    self.Walls[pos[0]][pos[1]][pos[2]][2] = None
                    pos[2] += 1

                else:
                    destroy(self.Walls[pos[0]][pos[1]][pos[2] - 1][2])
                    self.Walls[pos[0]][pos[1]][pos[2] - 1][2] = None
                    pos[2] -= 1

            # endregion

            # region Otherwise, backtrack

            else:
                pos = unvisitied_adjacent.pop()

            # endregion

        # Remove some walls randomly
        for i in range(round(random_deletion * total)):

            # Get X, Y, Z, and Direction
            wall_x = random.randrange(size)
            wall_y = random.randrange(size)
            wall_z = random.randrange(size)
            wall_dir = random.randrange(3)

            # Check if Wall Exists
            if (self.Walls[wall_x][wall_y][wall_z][wall_dir] != None):
                destroy(self.Walls[wall_x][wall_y][wall_z][wall_dir])
                self.Walls[wall_x][wall_y][wall_z][wall_dir] = None

        print(self.ladders)

        # endregion

        # region Point Creation

        # How many total points there are
        self.total_points = round(points_per_square * total)

        print(self.total_points)

        # How many points have been gotten
        self.current_points = 0

        # A list of all points
        self.points = []

        # Create a matrix of all possible point spots
        remaining_points = [(x, y, z) for x in range(self.size) for y in range(self.size) for z in range(self.size)]

        # Remove the starting position
        del remaining_points[0]

        # Create a point randomly for each pps
        for i in range(self.total_points):
            self.points.append(Point(position=remaining_points[random.randrange(remaining_points.__len__())]))

            # endregion

            # region Enemy Creation

            # A list of all enemies
            self.enemies = []

            # Create a matrix of all possible enemy spots
            remaining_spaces = [(x, y, z) for x in range(self.size) for y in range(self.size) for z in range(self.size)]

            # Remove the starting positions
            del remaining_spaces[0]

            # Create an enemy for each layer
            for _ in range(enemies_per_layer * self.size):
                space = random.randrange(remaining_spaces.__len__())
                # self.enemies.append(Enemy(self, position=remaining_spaces[space]))
                del remaining_spaces[space]

            # endregion

        # endregion

    def set_visible_layer(self, layer):

        # Set Wall Visibility
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    if (y > layer):
                        if (self.Walls[x][y][z][0] != None):
                            self.Walls[x][y][z][0].alpha = 0
                        if (self.Walls[x][y-1][z][1] != None):
                            self.Walls[x][y-1][z][1].alpha = 0
                        if (self.Walls[x][y][z][2] != None):
                            self.Walls[x][y][z][2].alpha = 0
                    else:
                        if (self.Walls[x][y][z][0] != None):
                            self.Walls[x][y][z][0].alpha = 1
                        if (self.Walls[x][y-1][z][1] != None):
                            self.Walls[x][y-1][z][1].alpha = 1
                        if (self.Walls[x][y][z][2] != None):
                            self.Walls[x][y][z][2].alpha = 1

        # Set Barrier Visibility
        for x in range(self.size ** 2):
            if (x >= (layer + 1) * self.size):
                self.Barriers_x[x][0].alpha = 0
                self.Barriers_x[x][1].alpha = 0
            else:
                self.Barriers_x[x][0].alpha = 1
                self.Barriers_x[x][1].alpha = 1

        # Set Barrier Visibility
        for z in range(self.size ** 2):
            if (z >= (layer + 1) * self.size):
                self.Barriers_z[z][0].alpha = 0
                self.Barriers_z[z][1].alpha = 0
            else:
                self.Barriers_z[z][0].alpha = 1
                self.Barriers_z[z][1].alpha = 1

        # Set Point Visibility
        for pt in self.points:
            if (pt.y > layer):
                pt.alpha = 0
            else:
                pt.alpha = 1

        # Set Ladder Visibility
        for ladder in self.ladder_list:
            if (ladder.y > layer):
                ladder.alpha = 0
            else:
                ladder.alpha = 1