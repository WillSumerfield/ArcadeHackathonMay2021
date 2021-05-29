from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from block import Block
from maze import Maze
from player import Player

# Create Game App
app = Ursina()

# region Build the World

maze = Maze(20)

# endregion

# region Player

player = Player()

# endregion

# region Camera

camera.position = (0, 2, 0)
camera.rotation = (70, 90, 0)

# endregion

# region HUD



# endregion

# region On Update

def update():
    if (held_keys['escape']):
        exit()


# endregion

# Run the Game
app.run()
