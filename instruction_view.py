import arcade
import game_view


class InstructionView(arcade.View):

    def __init__(self):
        super().__init__()

        self.controls_list = arcade.SpriteList()

        self.controls_sprite = arcade.Sprite("images/controls.png")
        self.controls_sprite.center_x = 600
        self.controls_sprite.center_y = 360

        self.controls_list.append(self.controls_sprite)

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        self.controls_sprite.position = (
            self.window.width / 2,
            self.window.height / 2 - 180
        )

    def on_draw(self):
        self.clear()

        self.controls_list.draw()

        arcade.draw_text(
            "Space Invaders",
            self.window.width / 2,
            self.window.height - 350,
            arcade.color.WHITE,
            font_size=50,
            font_name="VCR OSD Mono",
            anchor_x="center"
        )

        arcade.draw_text(
            "Click to Start",
            self.window.width / 2,
            self.window.height - 425,
            arcade.color.WHITE,
            font_size=20,
            font_name="VCR OSD Mono",
            anchor_x="center"
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        my_game_view = game_view.GameView()
        my_game_view.setup()
        self.window.show_view(my_game_view)