from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from block import Block
from maze import Maze
from player import Player
import os
from playsound import playsound

# Create Game App
app = Ursina()

# region Build the World

maze = Maze(20)

# endregion

# region Player

player = Player(maze)

# endregion

# region Camera

camera.position = (-6, 10, 0)
camera.rotation = (60, 90, 0)

# endregion

# region HUD

# endregion

# region On Update

def update():
    if (held_keys['escape']):
        exit()


# endregion

# region Music

#playsound(os.path.join("music", "pacman-theme.mp3"))

# endregion

# Run the Game
app.run()
