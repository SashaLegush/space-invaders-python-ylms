import arcade

from constants import *
import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path


class EnemyInvader(arcade.Sprite):
    def __init__(self, texture_1, texture_2):
        super().__init__()
        self.texture_1 = texture_1
        self.texture_2 = texture_2
        self.time = 0
        self.dead = False
        self.score = 0
        self.trigger_game_over = False

        self.texture = self.texture_1
        self.empty_texture = arcade.load_texture(resource_path("images/empty.png"))

    def on_update(self, dt):
        self.time += dt

        if not self.dead and self.center_y <= GAME_OVER_Y:
            self.dead = True
            self.trigger_game_over = True
            return

        if self.dead:
            if self.time >= 0.5:
                self.texture = self.empty_texture
            return

        t = int(self.time * 2)
        if t % 2 == 0:
            self.texture = self.texture_1
        else:
            self.texture = self.texture_2

    def explode(self):
        self.explode_texture = arcade.load_texture(resource_path("images/enemy_explosion.png"))
        self.dead = True
        self.time = 0
        self.color = ENEMY_EXPLOSION_COLOR