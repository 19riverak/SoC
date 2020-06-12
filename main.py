import arcade
import random
import os
from arcade.gui import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Get to Know the Root Glen"
SPEED=8

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AMAZON)
        self.tree_list=None #Why do you have to create empty properties ahead of time for sprites?
        self.kid=None

    def setup(self):
        self.tree_list=arcade.SpriteList()

        for x in range(0, 5):
            x = random.randrange(SCREEN_WIDTH / 10, SCREEN_WIDTH * 9/10 + 1)
            y = random.randrange(SCREEN_HEIGHT / 10, SCREEN_HEIGHT * 9 / 10 + 1)
            while SCREEN_WIDTH*3/10<=x<=SCREEN_WIDTH*7/10 and SCREEN_HEIGHT*3/10<=y<=SCREEN_HEIGHT*7/10:
                x = random.randrange(SCREEN_WIDTH / 5, SCREEN_WIDTH * 4/5 + 1)
                y = random.randrange(SCREEN_HEIGHT / 5, SCREEN_HEIGHT * 4 / 5 + 1)
            tree=arcade.Sprite("../images/tree.png", scale=.05, center_x=x, center_y=y)
            self.tree_list.append(tree)
        self.kid=arcade.Sprite("../images/kid.png", scale=.1, center_x=400, center_y=350)

    def on_draw(self):#Does the on draw function execute constantly, or just once at first?
        arcade.start_render() #What does this do?
        self.tree_list.draw()
        self.kid.draw()
        self.discover = arcade.check_for_collision_with_list(self.kid, self.tree_list)
        for x in self.discover:  #These 3 lines also work if in on update. Does it matter?
            game_view= QuestionView()
            game_view.setup()
            self.window.show_view(game_view)

    def on_update(self,time):
        self.kid.update()


    def on_key_press(self, key, mod): #What is mod?
        if key==arcade.key.LEFT:
            self.kid.change_x= -SPEED
        elif key==arcade.key.RIGHT:
            self.kid.change_x= +SPEED
        elif key == arcade.key.UP:
            self.kid.change_y = +SPEED
        elif key == arcade.key.DOWN:
            self.kid.change_y = -SPEED

    def on_key_release(self, key, mod): #What is mod?
        if key==arcade.key.LEFT:
            self.kid.change_x= 0
        elif key==arcade.key.RIGHT:
            self.kid.change_x= 0
        elif key == arcade.key.UP:
            self.kid.change_y = 0
        elif key == arcade.key.DOWN:
            self.kid.change_y = 0

class ButtonA(TextButton):
    def __init__(self, game, x=0, y=0, width=100, height=40, text="ButtonA", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game=game
 #   def on_press(self):
  #      self.pressed=True
 #   def on_release(self):
  #      if self.pressed:
   #         game_view = GameView()
    #        game_view.setup()
     #       self.window.show_view(game_view)
      #      self.pressed=False

class QuestionView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)
        self.leaf=None
        self.theme=None

    def set_button_textures(self):
        normal="../images/Normal.png"
        self.theme.add_button_textures(normal)

    def setup_theme(self):
        self.theme=Theme()
        self.theme.set_font(40, arcade.color.WHITE)
        self.set_button_textures()

    def set_buttons(self):
        self.button_list.append(ButtonA(self, SCREEN_WIDTH * 3/10, SCREEN_HEIGHT * 1/4, int(SCREEN_WIDTH/3), int(SCREEN_HEIGHT*3/20), theme=self.theme))

    def setup(self):
        leaf_dict={"maple": "../images/maple.jpg", "oak": "../images/oak.jpg", "birch": "../images/birch.jpg"}
        random_leaf=random.choice(list(leaf_dict.values()))
        self.leaf = arcade.Sprite(random_leaf, scale=1, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT * 3/5)
        self.setup_theme()
        self.set_buttons()

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        arcade.draw_text("What kind of tree leaf is shown?", SCREEN_WIDTH/2, SCREEN_HEIGHT*9/10, color=arcade.color.WHITE, font_size=40, anchor_x="center")
        self.leaf.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        #if ButtonA.pressed:
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()

if __name__=="__main__":
    main()
