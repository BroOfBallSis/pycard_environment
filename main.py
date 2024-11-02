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

if __name__ == "__main__":
    # 创建战斗实例
    battle = Battle()

    # 初始化战斗
    battle.initialize_battle()

    # 进入主循环
    battle.main_loop()
