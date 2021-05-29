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

            # Set Wall Based on Direction
            if (direction == Directions.FORWARD):
                self.position = position + (0.5,0,0)
                self.scale = (0.1,1,1)
                self.texture='texture_wall'
                self.color = color.white

            elif (direction == Directions.BACKWARD):
                self.position = position + (-0.5,0,0)
                self.scale = (0.1,1,1)
                self.color = color.white

            elif (direction == Directions.LEFT):
                self.position = position + (0,0,-0.5)
                self.scale = (1,1,0.1)
                self.color = color.white

            elif (direction == Directions.RIGHT):
                self.position = position + (0,0,0.5)
                self.scale = (1,1,0.1)
                self.color = color.white

            elif (direction == Directions.UP):
                self.position = position + (0,0.5,0)
                self.scale = (1,0.1,1)
                self.color = color.black

            else:
                self.position = position + (0,-0.5,0)
                self.scale = (1,0.1,1)
                self.color = color.black

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

