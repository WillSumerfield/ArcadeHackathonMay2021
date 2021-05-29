from ursina import *
from directions import Directions


class Block:

    class Wall(Button):

        def __init__(self,position,direction):
            super().__init__(
                parent=scene,
                model='cube',
                origin_y=0.5,
                origin=(0,0,0),
                alpha=1
            )



    def __init__(self, position=(0, 0, 0)):
        self.position = position

        # Create Walls
        walls = [
            self.Wall(position, Directions.FORWARD),
            self.Wall(position, Directions.BACKWARD),
            self.Wall(position, Directions.LEFT),
            self.Wall(position, Directions.RIGHT),
            #self.Wall(position, Directions.UP),
            self.Wall(position, Directions.DOWN)
        ]

