from ursina import *
from block import Block

# Directions in 2 Dimensions
Dir2D = enumerate(["up", "down", "left", "right"])


class MazeBlock:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = [True, True, True, True, True, True]


class Maze:

    def __init__(self, size, TwoDimension=True):

        # Instance Variables
        self.size = size
        self.grid = [[MazeBlock(i, ii) for i in range(size)] for ii in range(size)]

        # Method Variables
        open_adjacent = []
        visited = 0
        total = size * size
        position = [0,0]

        # Carve Out Maze
        #while (visited < total):
        #    self.grid[position[0]][position[1]]

        # Maze 2D4
        if (TwoDimension):
            for i in range(size):
                for ii in range(size):
                    block = Block(position=(i, 0, ii))
