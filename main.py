import sys
import os

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
