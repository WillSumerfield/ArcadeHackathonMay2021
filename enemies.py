from ursina import  *
import random


def update():
            random_enemy.x += random.randint(1,4)* time.dt
            slow_enemy.x += 1 * time.dt
            speedy_enemy.x += 6* time.dt

app = Ursina()
#enemy=Entity(model='quad', color=color.orange, scale = (2,5), position = (5,1))

random_enemy=Entity(model='quad',texture='./static/random_enemy.png',scale=2,position = (-10,0))
slow_enemy=Entity(model='quad',texture='./static/slow_enemy.png',scale=2,position = (-10,2))
speedy_enemy=Entity(model='quad',texture='./static/speedy_enemy.png',scale=2,position = (-10,3))
app.run()