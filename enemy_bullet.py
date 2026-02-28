import arcade
from constants import *
import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path


class EnemyBullet(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture(resource_path("images/enemy_bullet.png"))
        self.scale = SPRITE_SCALING_LASER

    def on_update(self, dt):
        self.time += dt
        t = int(self.time * 8)
        t2 = t % 4
        if t2 == 0:
            self.texture = self.texture_1
        elif t2 == 1:
            self.texture = self.texture_2
        elif t2 == 2:
            self.texture = self.texture_3
        elif t2 == 3:
            self.texture = self.texture_2

