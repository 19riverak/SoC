import arcade
import random
import os
from arcade.gui import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Get to Know the Root Glen"
SPEED=8

class IntroView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_SEA_GREEN)

    def setup(self):
        self.rootglen = arcade.Sprite("../images/rootglen.jpg", scale=.8, center_x=SCREEN_WIDTH/2, center_y=SCREEN_HEIGHT*9/20)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Get to Know the", SCREEN_WIDTH/2, SCREEN_HEIGHT*17/20, arcade.color.NAVY_BLUE, 60, bold=True, anchor_x="center")
        arcade.draw_text("Root Glen!", SCREEN_WIDTH / 2, SCREEN_HEIGHT*15/20, arcade.color.NAVY_BLUE, 60, bold=True, anchor_x="center")
        arcade.draw_text("Learn to identify tree leaves.", SCREEN_WIDTH/2, SCREEN_HEIGHT*13/20, arcade.color.NAVY_BLUE, 45, anchor_x="center")
        arcade.draw_text("Use the up, down, left, and right arrow keys", SCREEN_WIDTH/2, SCREEN_HEIGHT*4/20, arcade.color.CHARCOAL, 30, anchor_x="center")
        arcade.draw_text("to move to a tree.", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3/20, arcade.color.CHARCOAL, 30, anchor_x="center")
        arcade.draw_text("Click to begin the game.", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 1.5 / 20, arcade.color.CHARCOAL, 30, anchor_x="center")
        self.rootglen.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        start_view = GameView()
        self.window.show_view(start_view)
        start_view.setup()

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
                x = random.randrange(SCREEN_WIDTH / 10, SCREEN_WIDTH * 9 / 10 + 1)
                y = random.randrange(SCREEN_HEIGHT / 10, SCREEN_HEIGHT * 9 / 10 + 1)
            tree=arcade.Sprite("../images/tree.png", scale=.05, center_x=x, center_y=y)
            self.tree_list.append(tree)
        self.kid=arcade.Sprite("../images/kid.png", scale=.1, center_x=400, center_y=350)

    def on_draw(self):#Does the on draw function execute constantly, or just once at first?
        arcade.start_render() #What does this do?
        self.tree_list.draw()
        self.kid.draw()
        self.question_counter=f"Trees Identified: {QuestionCounter.number_correct}"
        arcade.draw_text(self.question_counter, SCREEN_WIDTH * 2/3, SCREEN_HEIGHT*14/15, arcade.color.WHITE, 25)
        self.level_counter=f"Level: {QuestionCounter.level}"
        arcade.draw_text(self.level_counter, SCREEN_WIDTH * 2 / 3, SCREEN_HEIGHT * 13 / 15, arcade.color.WHITE, 25)
        self.discover = arcade.check_for_collision_with_list(self.kid, self.tree_list)
        for x in self.discover:  #These 3 lines also work if in on update. Does it matter?
            game_view= QuestionView()
            game_view.setup()
            self.window.show_view(game_view)

    def on_update(self,time):
        self.kid.update()

        if QuestionCounter.number_correct>=(8+12*(QuestionCounter.level*(QuestionCounter.level-1)/2)) and QuestionCounter.level<=2:
            QuestionCounter.level+=1
            QuestionCounter.number_correct=0
            start_view = LevelUpView()
            self.window.show_view(start_view)

        if QuestionCounter.number_correct>=(8+12*(QuestionCounter.level*(QuestionCounter.level-1)/2)) and QuestionCounter.level==3:
            start_view = YouWinView()
            self.window.show_view(start_view)
            start_view.setup()

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

class CorrectButton(TextButton):
    def __init__(self, game, x=0, y=0, width=100, height=40, text=None, theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game=game
        #self.text=text
        self.pressed=False
    def on_press(self):
        self.pressed=True

class IncorrectButton(TextButton):
    def __init__(self, game, x=0, y=0, width=100, height=40, text=None, theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game=game
        self.pressed=False

class QuestionView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)
        self.leaf=None
        self.theme=None
        self.option1=None
        self.incorrect_option=None

    def set_button_textures(self):
        normal="../images/Normal.png"
        #clicked="../images/Clicked.png"
        self.theme.add_button_textures(normal)

    def setup_theme(self):
        self.theme=Theme()
        self.theme.set_font(25, arcade.color.NAVY_BLUE)
        self.set_button_textures()

    def make_question(self):
        self.leaf_dict1 = {"northern red oak": "../images/NorthernRedOak.png", "sugar maple": "../images/SugarMaple.png", "sweet birch":"../images/SweetBirch.png", "bitternut hickory": "../images/BitternutHickory.png"}
        self.more_leaves2 = {"American hornbeam":"../images/AmericanHornbeam.png", "beech":"../images/Beech.png", "black walnut": "../images/BlackWalnut.png", "quaking aspen": "../images/QuakingAspen.png", "tuliptree":"../images/Tuliptree.png", "black cherry":"../images/BlackCherry.png"}
        self.leaf_dict2 = self.leaf_dict1.copy()
        self.leaf_dict2.update(self.more_leaves2)
        self.more_leaves3 = {"American sycamore":"../images/AmericanSycamore.png", "black willow": "../images/BlackWillow.png", "common hoptree": "../images/CommonHoptree.png", "common horsechestnut": "../images/CommonHorsechestnut.png", "flowering dogwood":"../images/FloweringDogwood.png", "sassafras":"../images/Sassafras.png", "white ash":"../images/WhiteAsh.png", "white poplar":"../images/WhitePoplar.png", "yellow birch": "../images/YellowBirch.png"}
        self.leaf_dict3 = self.leaf_dict2.copy()
        self.leaf_dict3.update(self.more_leaves3)
        self.leaf_list=(self.leaf_dict1, self.leaf_dict2, self.leaf_dict3)
        self.leaf_dict_for_current_level=self.leaf_list[QuestionCounter.level - 1]
        self.random_leaf = random.choice(list(self.leaf_dict_for_current_level.keys()))
        self.random_leaf_image = self.leaf_dict_for_current_level[self.random_leaf]
        self.leaf_dict_for_current_level.pop(self.random_leaf)

    def set_buttons(self):
        self.coordinate_dict={"top_left": [int(SCREEN_WIDTH * 2.8 / 10), int(SCREEN_HEIGHT * 1 / 4)], "top_right": [int(SCREEN_WIDTH * 7.2 / 10), int(SCREEN_HEIGHT * 1 / 4)], "bottom_left": [int(SCREEN_WIDTH * 2.8 / 10), int(SCREEN_HEIGHT * 1 / 9)], "bottom-right": [int(SCREEN_WIDTH * 7.2 / 10), int(SCREEN_HEIGHT * 1 / 9)]}
        self.position=random.choice(list(self.coordinate_dict.keys()))
        self.coordinate=self.coordinate_dict[self.position]
        x=self.coordinate[0]
        y=self.coordinate[1]
        self.option1= CorrectButton(self, x, y, int(SCREEN_WIDTH / 2.5), int(SCREEN_HEIGHT * 3 / 25), self.random_leaf, theme=self.theme)
        self.button_list.append(self.option1)
        self.coordinate_dict.pop(self.position)

        for i in range (0,3):
            self.position = random.choice(list(self.coordinate_dict.keys()))
            self.coordinate = self.coordinate_dict[self.position]
            x = self.coordinate[0]
            y = self.coordinate[1]
            self.incorrect_leaf=random.choice(list(self.leaf_dict_for_current_level.keys()))
            self.leaf_dict_for_current_level.pop(self.incorrect_leaf)
            self.incorrect_option = IncorrectButton(self, x, y, int(SCREEN_WIDTH / 2.5), int(SCREEN_HEIGHT * 3 / 25), self.incorrect_leaf, theme=self.theme)
            self.button_list.append(self.incorrect_option)
            self.coordinate_dict.pop(self.position)

    def setup(self):
        self.make_question()
        self.leaf = arcade.Sprite(self.random_leaf_image, scale=1, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT * 3/5)
        self.setup_theme()
        self.set_buttons()

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        arcade.draw_text("What kind of tree leaf is shown?", SCREEN_WIDTH/2, SCREEN_HEIGHT*9/10, color=arcade.color.WHITE, font_size=40, anchor_x="center")
        self.leaf.draw()

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
       if self.option1.pressed:
            QuestionCounter.number_correct += 1
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

class QuestionCounter:
    number_correct=0
    level=1

class LevelUpView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLUE_VIOLET)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("CONGRATULATIONS!", SCREEN_WIDTH/2, SCREEN_HEIGHT*4/5, arcade.color.WHITE, 60, bold=True, anchor_x="center")
        arcade.draw_text(f"Get ready for LEVEL {QuestionCounter.level}.", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, arcade.color.LIME_GREEN, 45, anchor_x="center")
        arcade.draw_text("Click to proceed.", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 1 / 7, arcade.color.WHITE, 30, anchor_x="center")

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        start_view = GameView()
        self.window.show_view(start_view)
        start_view.setup()

class YouWinView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.PASTEL_PURPLE)

    def setup(self):
        self.rootglen2 = arcade.Sprite("../images/rootglen2.jpg", scale=.8, center_x=SCREEN_WIDTH/2, center_y=SCREEN_HEIGHT*9/20)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("You Win!", SCREEN_WIDTH/2, SCREEN_HEIGHT*17/20, arcade.color.WHITE, 60, bold=True, anchor_x="center")
        arcade.draw_text("You are now an expert", SCREEN_WIDTH/2, SCREEN_HEIGHT*15/20, arcade.color.LIME_GREEN, 45, anchor_x="center")
        arcade.draw_text("in tree leaf identification.", SCREEN_WIDTH/2, SCREEN_HEIGHT*13.5/20, arcade.color.LIME_GREEN, 45, anchor_x="center")
        arcade.draw_text("Thanks for playing!", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 1 / 7, arcade.color.WHITE, 30, anchor_x="center")
        self.rootglen2.draw()

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = IntroView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()

if __name__=="__main__":
    main()
