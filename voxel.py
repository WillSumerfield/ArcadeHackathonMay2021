from ursina import *


class Voxel(Button):

    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture='white_cube',
            color=color.white,
            highlight_color=color.dark_gray
        )

    def input(self, key):
        if self.hovered:
            if (key == 'left mouse down'):
                voxel = Voxel(position=self.position + mouse.normal)
            elif (key == 'right mouse down'):
                destroy(self)
