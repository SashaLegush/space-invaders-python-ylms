import random
import arcade
from pyglet.math import Vec2

from enemy_bullet import EnemyBullet
from constants import *
from enemy_invader import EnemyInvader
import instruction_view
import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        self.player_list = None
        self.enemy_list = None
        self.player_bullet_list = None
        self.enemy_bullet_list = None
        self.shield_list = None

        self.enemy_textures = None

        self.game_state = PLAY_GAME

        self.game_over = False

        self.player_sprite = None
        self.score = 0
        self.lives = 3
        self.death_pause = 0

        self.filter_on = True

        self.enemy_change_x = -ENEMY_SPEED

        self.gun_sound = arcade.load_sound(resource_path("sound/shoot.wav"))
        self.hit_sound = arcade.load_sound(resource_path("sound/invaderkilled.wav"))
        self.player_explosion = arcade.load_sound(resource_path("sound/invaderkilled.wav"))
        self.game_over_sound = arcade.load_sound(resource_path("sound/explosion.wav"))

        arcade.set_background_color(arcade.color.BLACK)


    def setup_level_one(self):
        column_count = 10
        x_start = 380
        x_spacing = 90

        row_count = 5
        y_start = 720
        y_spacing = 60
        for column in range(column_count):
            x = x_start + x_spacing * column
            for row in range(row_count):
                y = y_start + y_spacing * row
                score = 0

                enemy_texture = arcade.load_texture(resource_path("images/enemy.png"))

                row_scores = {0: 10, 1: 10, 2: 20, 3: 20, 4: 30}

                score = row_scores.get(row, 10)
                texture1 = enemy_texture
                texture2 = enemy_texture
                enemy = EnemyInvader(texture1, texture2)
                enemy.score = score
                enemy.scale = SPRITE_SCALING_enemy

                enemy.center_x = x
                enemy.center_y = y

                self.enemy_list.append(enemy)

    def make_shield(self, x_start):
        shield_block_width = 5
        shield_block_height = 10
        shield_width_count = 25
        shield_height_count = 7
        y_start = 170
        for x in range(x_start,
                       x_start + shield_width_count * shield_block_width,
                       shield_block_width):
            for y in range(y_start,
                           y_start + shield_height_count * shield_block_height,
                           shield_block_height):
                shield_sprite = arcade.SpriteSolidColor(shield_block_width,
                                                        shield_block_height,
                                                        arcade.color.WHITE)
                shield_sprite.center_x = x
                shield_sprite.center_y = y
                self.shield_list.append(shield_sprite)

    def setup(self):
        self.game_state = PLAY_GAME

        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.shield_list = arcade.SpriteList()

        self.score = 0

        self.player_sprite = arcade.Sprite(resource_path("images/player.png"), SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 60
        self.player_sprite.color = PLAYER_COLOR
        self.player_list.append(self.player_sprite)

        for x in range(140, 1200, 270):
            self.make_shield(x)

        self.setup_level_one()

    def draw(self):
        self.enemy_list.draw(pixelated=True)
        self.player_bullet_list.draw(pixelated=True)
        self.enemy_bullet_list.draw(pixelated=True)
        self.shield_list.draw(pixelated=True)
        self.player_list.draw(pixelated=True)

        arcade.draw_text(f"Score: {self.score:04}",
                         30, 30,
                         arcade.color.WHITE,
                         24,
                         font_name="VCR OSD Mono")

        arcade.draw_text(f"Lives: {self.lives}",
                         30, SCREEN_HEIGHT - 35,
                         arcade.color.WHITE,
                         24,
                         font_name="VCR OSD Mono")

        if self.game_state == GAME_OVER:
            arcade.draw_text("GAME OVER", self.window.width / 2, self.window.height / 2 + 20,
                             arcade.color.WHITE, font_size=50, font_name="VCR OSD Mono", anchor_x="center")

            arcade.draw_text("Press space", self.window.width / 2, self.window.height / 2 - 35,
                             arcade.color.WHITE, font_size=50, font_name="VCR OSD Mono", anchor_x="center")

            self.window.set_mouse_visible(True)

    def draw(self):
        if self.game_state == PLAY_GAME:
            self.enemy_list.draw(pixelated=True)
            self.player_bullet_list.draw(pixelated=True)
            self.enemy_bullet_list.draw(pixelated=True)
            self.shield_list.draw(pixelated=True)
            self.player_list.draw(pixelated=True)

        arcade.draw_text(f"Score: {self.score:04}",
                         30, 30,
                         arcade.color.WHITE,
                         24,
                         font_name="VCR OSD Mono")

        arcade.draw_text(f"Lives: {self.lives}",
                         30, SCREEN_HEIGHT - 35,
                         arcade.color.WHITE,
                         24,
                         font_name="VCR OSD Mono")

        if self.game_state == GAME_OVER:
            arcade.draw_text("GAME OVER",
                             SCREEN_WIDTH / 2,
                             SCREEN_HEIGHT / 2 + 20,
                             arcade.color.WHITE,
                             50,
                             anchor_x="center",
                             font_name="VCR OSD Mono")
            arcade.draw_text("Press Space",
                             SCREEN_WIDTH / 2,
                             SCREEN_HEIGHT / 2 - 35,
                             arcade.color.WHITE,
                             24,
                             anchor_x="center",
                             font_name="VCR OSD Mono")
        elif self.game_state == YOU_WIN:
            arcade.draw_text("YOU WIN!",
                             SCREEN_WIDTH / 2,
                             SCREEN_HEIGHT / 2 + 20,
                             arcade.color.LIGHT_GREEN,
                             50,
                             anchor_x="center",
                             font_name="VCR OSD Mono")
            arcade.draw_text("Press Space",
                             SCREEN_WIDTH / 2,
                             SCREEN_HEIGHT / 2 - 35,
                             arcade.color.LIGHT_GREEN,
                             24,
                             anchor_x="center",
                             font_name="VCR OSD Mono")

    def on_draw(self):
        self.clear()
        self.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.game_state == GAME_OVER:
            return

        self.player_sprite.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        if self.death_pause:
            return

        if len(self.player_bullet_list) < MAX_PLAYER_BULLETS:
            arcade.play_sound(self.gun_sound)
            bullet = arcade.Sprite(resource_path("images/player_bullet.png"), SPRITE_SCALING_LASER)
            bullet.color = PLAYER_COLOR
            bullet.change_y = PLAYER_BULLET_SPEED
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top
            self.player_bullet_list.append(bullet)

    def update_enemies(self):
        for enemy in self.enemy_list:
            enemy.center_x += self.enemy_change_x

        move_down = False
        for enemy in self.enemy_list:
            if enemy.right > RIGHT_ENEMY_BORDER and self.enemy_change_x > 0:
                self.enemy_change_x *= -1
                move_down = True
            if enemy.left < LEFT_ENEMY_BORDER and self.enemy_change_x < 0:
                self.enemy_change_x *= -1
                move_down = True

        if move_down:
            for enemy in self.enemy_list:
                enemy.center_y -= ENEMY_MOVE_DOWN_AMOUNT

    def cleanup(self):
        for sprite_list in [
            self.player_list,
            self.enemy_list,
            self.player_bullet_list,
            self.enemy_bullet_list,
            self.shield_list
        ]:
            if sprite_list:
                sprite_list.clear()

    def allow_enemies_to_fire(self):
        x_spawn = []
        for enemy in self.enemy_list:
            if enemy.dead:
                continue
            chance = 3 + len(self.enemy_list) * 20

            if random.randrange(chance) == 0 and enemy.center_x not in x_spawn:
                bullet = EnemyBullet()
                bullet.change_y = -BULLET_SPEED
                bullet.center_x = enemy.center_x
                bullet.top = enemy.bottom
                self.enemy_bullet_list.append(bullet)
            x_spawn.append(enemy.center_x)

    def process_enemy_bullets(self):
        self.enemy_bullet_list.update()
        for bullet in self.enemy_bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.shield_list)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                for shield in hit_list:
                    shield.remove_from_sprite_lists()
                continue

            if arcade.check_for_collision_with_list(self.player_sprite, self.enemy_bullet_list):
                if self.lives > 0:
                    arcade.play_sound(self.player_explosion)
                    self.lives -= 1
                    self.enemy_bullet_list = arcade.SpriteList()
                    self.player_bullet_list = arcade.SpriteList()
                    self.death_pause = DEATH_PAUSE_TIME
                else:
                    self.game_state = GAME_OVER
                    arcade.play_sound(self.game_over_sound)
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

            if self.lives <= 0:
                self.game_state = GAME_OVER
                arcade.play_sound(self.game_over_sound)
                self.cleanup()

    def process_player_bullets(self):
        self.player_bullet_list.update()
        for bullet in self.player_bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.shield_list)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                for shield in hit_list:
                    shield.remove_from_sprite_lists()
                continue
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            for enemy in hit_list:
                if enemy.dead:
                    continue
                bullet.remove_from_sprite_lists()
                enemy.explode()
                self.score += enemy.score
                arcade.play_sound(self.hit_sound)

            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

    def on_update(self, dt):
        if self.game_state in (GAME_OVER, YOU_WIN):
            return

        if self.death_pause > 0:
            self.death_pause -= dt
            if self.death_pause < 0:
                self.death_pause = 0
            return

        for enemy in self.enemy_list:
            enemy.on_update(dt)

            if getattr(enemy, "trigger_game_over", False):
                self.game_state = GAME_OVER
                arcade.play_sound(self.game_over_sound)
                self.cleanup()
                return

        self.update_enemies()
        self.allow_enemies_to_fire()
        self.process_enemy_bullets()
        self.process_player_bullets()

        alive_enemies = [enemy for enemy in self.enemy_list if not getattr(enemy, "dead", False)]
        if len(alive_enemies) == 0 and self.game_state != GAME_OVER:
            self.game_state = YOU_WIN
            arcade.play_sound(self.hit_sound)

    def on_key_press(self, symbol: int, modifiers: int):
        if self.game_state in (GAME_OVER, YOU_WIN) and symbol == arcade.key.SPACE:
            my_game_view = instruction_view.InstructionView()
            self.window.show_view(my_game_view)
