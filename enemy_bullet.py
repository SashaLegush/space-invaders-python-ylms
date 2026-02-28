import arcade
from constants import *


class EnemyBullet(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("images/enemy_bullet.png")
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

