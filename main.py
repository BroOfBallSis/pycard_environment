import sys
import os
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

# 添加当前脚本所在的目录到sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 现在可以安全地导入模块了
from player.base_player import BasePlayer
from scene.local_battle import Battle

class Menu:
    def __init__(self, name, options, parent=None):
        self.name = name
        self.options = options
        self.parent = parent

    def display(self):
        print(f"\n{self.name}:")
        for index, option in enumerate(self.options, start=1):
            print(f"{index}. {option['text']}")
        if self.parent:
            print(f"{len(self.options) + 1}. 返回上一级")
        choice = input("\n请输入你的选择：")
        return self.handle_choice(choice)

    def handle_choice(self, choice):
        if choice.isdigit() and 1 <= int(choice) <= len(self.options):
            return self.options[int(choice) - 1]['action']()
        elif self.parent and choice == str(len(self.options) + 1):
            return self.parent.display()
        else:
            print("无效的选择，请重新输入。")
            return self.display()

class Game:
    def __init__(self):
        self.main_menu = Menu(
            "主菜单",
            [
                {"text": "进入教程", "action": self.tutorial_menu},
                {"text": "对战AI", "action": self.vs_ai_menu}
            ]
        )
        self.tutorial_menu = Menu(
            "教程内容",
            [
                {"text": "时间与韧性", "action": self.time_and_resilience_tutorial},
                {"text": "闪避与撤离", "action": self.evasion_and_retreat_tutorial}
            ],
            self.main_menu
        )
        self.pve_select_player_menu = Menu(
            "选择玩家角色",
            [
                {"text": "剑士", "action": self.warrior},
                {"text": "近卫", "action": self.guard},
                {"text": "自定义角色", "action": self.custom_character}
            ],
            self.main_menu
        )
        self.pve_select_enemy_menu = Menu(
            "选择敌人角色",
            [
                {"text": "剑士", "action": self.warrior},
                {"text": "近卫", "action": self.guard},
                {"text": "自定义角色", "action": self.custom_character}
            ],
            self.pve_select_player_menu
        )
        self.pve_menu = Menu(
            "开始对战",
            [
                {"text": "开始对战", "action": self.start_battle}
            ],
            self.pve_select_enemy_menu
        )

    def run(self):
        self.main_menu.display()

    def tutorial_menu(self):
        print("\n你选择了：教程")
        # 在这里添加教程内容
        return self.tutorial_menu.display()

    def vs_ai_menu(self):
        print("\n你选择了：对战AI")
        # 在这里添加对战AI内容
        return self.vs_ai_menu.display()

    def time_and_resilience_tutorial(self):
        print("\n你选择了：时间与韧性")
        # 在这里添加时间与韧性的教程内容

    def evasion_and_retreat_tutorial(self):
        print("\n你选择了：闪避与撤离")
        # 在这里添加闪避与撤离的教程内容

    def warrior(self):
        print("\n你选择了：剑士")
        # 在这里添加剑士角色的逻辑

    def guard(self):
        print("\n你选择了：近卫")
        # 在这里添加近卫角色的逻辑

    def custom_character(self):
        print("\n你选择了：自定义角色")
        # 在这里添加自定义角色的逻辑

    def start_battle(self):
        print("开始对战！")
        # 创建战斗实例
        battle = Battle(self.characters)

        # 初始化战斗
        battle.initialize_battle()

        # 进入主循环
        battle.main_loop()

if __name__ == "__main__":
    game = Game()
    game.run()
