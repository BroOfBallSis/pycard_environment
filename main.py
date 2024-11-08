import sys
import os

# 添加当前脚本所在的目录到sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 现在可以安全地导入模块了
from player.base_player import BasePlayer
from scene.base_battle import BaseBattle
from scene.tutorial.time_and_resilience_tutorial import TutorialBattle1
from scene.tutorial.dodge_and_retreat_tutorial import TutorialBattle2
from scene.main_menu import menu_dict, Menu, MenuItem
from utils.draw_text import color_text, clear_terminal, center_text


clear_terminal()
rights_statement = f"""
==========================================================
|{center_text("权益声明",56)}|
==========================================================
|{center_text("本软件的所有权益归 solaireli 所有。",56)}|
|{center_text("禁止任何形式的商业用途和盗版行为。",56)}|
|{center_text("任何违反上述规定的行为将追究法律责任。",56)}|
==========================================================
"""
print(rights_statement)
print("QQ 交流群: 685811874")
input(color_text("输入回车键接受并继续……", "gray"))
clear_terminal()


class Game:
    def __init__(self, menu_dict):
        self.characters = ["ch00001", "ch00001"]
        self.players = ["player", "BOT"]
        self.menu_dict = menu_dict
        self.current_menu = self.menu_dict["main_menu"]
        self.pass_time_and_resilience_tutorial = False
        self.pass_dodge_and_retreat_tutorial = False

    def run(self):
        self.current_menu.display(self)

    def navigate_to(self, menu_name, *args, **kwargs):
        if menu_name in self.menu_dict:
            self.current_menu = self.menu_dict[menu_name]
            return self.current_menu.display(self)
        elif hasattr(self, menu_name):
            method = getattr(self, menu_name)
            return method(*args, **kwargs)
        else:
            print(f"菜单 {menu_name} 不存在。")
            return self.current_menu.display(self)

    def time_and_resilience_tutorial(self):

        # 创建战斗实例
        battle = TutorialBattle1(self.players, ["th00001", "th00001"])

        # 初始化战斗
        battle.initialize_battle()

        # 进入主循环
        if battle.main_loop() and not self.pass_time_and_resilience_tutorial:
            old_text = menu_dict["tutorial_menu"].items[0].text
            menu_dict["tutorial_menu"].items[0].text = color_text(old_text, "gray")
            self.pass_time_and_resilience_tutorial = True

        del battle

    def dodge_and_retreat_tutorial(self):

        # 创建战斗实例
        battle = TutorialBattle2(self.players, ["th00001", "th00001"])

        # 初始化战斗
        battle.initialize_battle()

        # 进入主循环
        if battle.main_loop() and not self.pass_dodge_and_retreat_tutorial:
            old_text = menu_dict["tutorial_menu"].items[1].text
            menu_dict["tutorial_menu"].items[1].text = color_text(old_text, "gray")
            self.pass_dodge_and_retreat_tutorial = True

        del battle

    def select_character(self, character_id, player_index):
        self.characters[player_index] = character_id
        if player_index == 0:
            return self.navigate_to("pve_enemy_menu")
        else:
            return self.navigate_to("pve_start_menu")

    def start_battle(self):
        print("开始对战！")
        # 创建战斗实例
        battle = BaseBattle(self.players, self.characters)

        # 初始化战斗
        battle.initialize_battle()

        # 进入主循环
        battle.main_loop()

        del battle
        self.current_menu = self.menu_dict["main_menu"]


if __name__ == "__main__":

    game = Game(menu_dict)
    while True:
        game.run()
