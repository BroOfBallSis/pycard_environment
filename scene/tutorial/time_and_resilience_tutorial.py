from scene.base_battle import BaseBattle
from enum import Enum
from player.base_player import BasePlayer
from character.status.base_status import CharacterStatusType
import time
from utils.draw_text import color_text, clear_terminal
from utils.debug import print_memory_info
from scene.scene_define import BattlePhase
from card.base_card import BaseCard


class TutorialBattle1(BaseBattle):
    def __init__(self, characters):
        self.player1 = BasePlayer("player1", 1, "th00001", "terminal", self)
        self.player2 = BasePlayer("player2", 2, "th00001", "sword_ai", self)
        self.player_list = [self.player1, self.player2]
        self.player1.opponent = self.player2
        self.player2.opponent = self.player1
        self.round_cnt = 0
        self.turn_cnt = 0
        self.current_phase = BattlePhase.INITIALIZATION
        self.player1.card_manager.hand.append(BaseCard.from_json(self.player1, "a00007"))
        self.player2.card_manager.hand.append(BaseCard.from_json(self.player2, "a00001"))

    def main_loop(self):
        while not self.is_battle_over():

            # 轮开始
            self.start_round()

            while not self.is_round_over() and not self.is_battle_over():

                input(color_text("输入回车键继续……", "gray"))
                clear_terminal()

                # 回合开始
                self.start_turn()

                # 出牌阶段
                self.current_phase = BattlePhase.PLAY_PHASE
                if self.round_cnt == 1 and self.turn_cnt == 1:
                    print(f"\t{color_text('教程:','yellow')} 打出卡牌需要支付体力, \"长剑竖劈\" 将消耗 7点体力")
                    print(
                        f"\t{color_text('教程:','yellow')} {color_text('输入 [0] 并按回车键','yellow')}, 打出手牌中的 \"长剑竖劈\""
                    )
                if self.round_cnt == 1 and self.turn_cnt == 2:
                    print(f"\t{color_text('教程:','yellow')} 卡牌实际结算的时刻 等于 卡牌时间 + 延迟 + 其他效果")
                    print(
                        f"\t{color_text('教程:','yellow')} 你在上回合获得了 2点延迟,  时间3 的 \"长剑突刺\" 会在 时刻5 结算"
                    )
                    print(
                        f"\t{color_text('教程:','yellow')} {color_text('输入 [0] 并按回车键','yellow')}, 打出手牌中的 \"长剑突刺\""
                    )
                if self.round_cnt == 1 and self.turn_cnt == 3:
                    print(f"\t{color_text('教程:','yellow')} 为了展示 延迟 到达上限的情况, 手动将对手的 延迟 设置为 5")
                    self.player2.character.delay.set_value(5)
                    print(
                        f"\t{color_text('教程:','yellow')} {color_text('输入 [0] 并按回车键','yellow')}, 打出手牌中的 \"长剑突刺\""
                    )
                if self.round_cnt == 1 and self.turn_cnt == 4:
                    print(f"\t{color_text('教程:','yellow')} 你的对手处于 \"破绽\"状态, 放心地采取进攻, 赢得比赛胜利")
                    print(
                        f"\t{color_text('教程:','yellow')} {color_text('输入 [0] 并按回车键','yellow')}, 打出手牌中的 \"长剑竖劈\""
                    )
                for player in self.player_list:
                    self.play_phase(player)

                # 结算阶段
                self.current_phase = BattlePhase.RESOLVE_PHASE
                self.resolve_phase()
                # 回合 1
                if self.round_cnt == 1 and self.turn_cnt == 1:
                    self.player1.card_manager.hand = []
                    self.player2.card_manager.hand = []
                    self.player1.card_manager.hand.append(BaseCard.from_json(self.player1, "a00004"))
                    self.player2.card_manager.hand.append(BaseCard.from_json(self.player2, "a00007"))
                # 回合 2
                if self.round_cnt == 1 and self.turn_cnt == 2:
                    self.player1.card_manager.hand = []
                    self.player2.card_manager.hand = []
                    self.player1.card_manager.hand.append(BaseCard.from_json(self.player1, "a00004"))
                    self.player2.card_manager.hand.append(BaseCard.from_json(self.player2, "a00007"))
                # 回合 3
                if self.round_cnt == 1 and self.turn_cnt == 3:
                    self.player1.card_manager.hand = []
                    self.player2.card_manager.hand = []
                    self.player1.card_manager.hand.append(BaseCard.from_json(self.player1, "a00007"))
                    self.player2.card_manager.hand.append(BaseCard.from_json(self.player2, "a00007"))
                # 回合结束
                self.end_turn()
                if self.round_cnt == 1 and self.turn_cnt == 1:
                    print(f"\t{color_text('教程:','yellow')} 卡牌上的 '时间' 表明了在哪个 '时刻' 结算卡牌的效果")
                    print(f"\t{color_text('教程:','yellow')} 结算完成后, 后手方会增加等于时刻差值的 '延迟'")
                if self.round_cnt == 1 and self.turn_cnt == 2:
                    print(
                        f"\t{color_text('教程:','yellow')} 每个时刻结束, 如果角色的 '韧性' 小于等于0, 角色获得 \"打断\"状态"
                    )
                    print(f"\t{color_text('教程:','yellow')} \"打断\"状态下, 角色不再发起 自身出牌 的效果结算")
                if self.round_cnt == 1 and self.turn_cnt == 3:
                    print(f"\t{color_text('教程:','yellow')} 如果角色的 '延迟' 大于等于上限值, 角色获得 \"破绽\"状态")
                    print(
                        f"\t{color_text('教程:','yellow')} \"破绽\"状态下, 角色会跳过 出牌阶段 , 直接打出一张 时间6 的 \"破绽\" "
                    )

            # 弃牌阶段
            if not self.is_battle_over():
                input(color_text("输入回车键继续……", "gray"))
                clear_terminal()
                self.current_phase = BattlePhase.DISCARD_PHASE
                for player in self.player_list:
                    self.discard_phase(player)
                input(color_text("输入回车键继续……", "gray"))
                clear_terminal()

        self.conclude_battle()


if __name__ == "__main__":
    # 创建战斗实例
    battle = TutorialBattle1(["ch00001", "ch00001"])

    # 初始化战斗
    battle.initialize_battle()

    # 进入主循环
    battle.main_loop()
