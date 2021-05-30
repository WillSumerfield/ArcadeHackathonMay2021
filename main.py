from ursina import *
from maze import Maze
from player import Player
from enemies import Enemy
import os
from playsound import playsound

# Create Game App
app = Ursina()

# region Build the World

maze = Maze(5, two_dimension=False)

# endregion

# region Player

player = Player(maze)

lives = 3

# endregion

# region Camera

camera.position = (-6, 10, 0)
camera.rotation = (60, 90, 0)

# endregion

# region HUD

# Text
Points = Text(f"Points: {maze.total_points - maze.current_points}", size=0.05, position=(-0.85, 0.45))

# Ursina
window.fps_counter.enabled = False
window.exit_button.visible = False
window.title = "PacMun - 3D"
window.cog_menu.enabled = False
window.fullscreen = True

# endregion

# region Gameover

def gameover():
    exit()


# endregion

# region On Update

def update():
    if (held_keys['escape']):
        exit()

    # region HUD Updates

    Points.text = f"Remaining Points: {maze.total_points - maze.current_points}"

    # endregion

    # region Check for Gameover

    if (player.gameover):
        gameover()

    #endregion


# endregion

# region Music

#playsound(os.path.join("music", "pacman-theme.mp3"))

# endregion

# Run the Game
app.run()
