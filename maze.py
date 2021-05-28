from ursina import *
from voxel import Voxel

# Directions in 2 Dimensions
Dir2D = enumerate(["up", "down", "left", "right"])

class Block:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = [True, True, True, True]

class Maze:

    def __init__(self, size):

        # Instance Variables
        self.size = size
        self.grid = [[Block(i, ii) for i in range(size)] for ii in range(size)]

        # Method Variables
        open_adjacent = []
        visited = 0
        total = size * size
        position = [0,0]

        # Carve Out Maze
        while (visited < total):
            self.grid[position[0],position[1]]

        # Create 2D Maze
        for i in range(size):
            for ii in range(size):
                voxel = Voxel(position=(i, 0, ii))
