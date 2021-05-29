from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from voxel import Voxel
import os
from playsound import playsound

# Create Game App
app = Ursina()

# region Build the World



# endregion

# region Player

player = FirstPersonController()
player.model = 'sphere'
player.color = color.yellow
player.scale = (0.8, 0.8, 0.8)
player.origin_y = 0

# endregion

# region Camera

camera.position = (0, 1, -5)
camera.rotation = (30, 0, 0)


# endregion

# region HUD

# endregion

# region On Update
def update():
    if (held_keys['escape']):
        exit()


# endregion



#music

playsound(os.path.join("music", "pacman-theme.mp3"))  

# Run the Game
app.run()
