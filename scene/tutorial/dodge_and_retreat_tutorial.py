from scene.base_battle import BaseBattle
from player.base_player import BasePlayer
from utils.draw_text import color_text, clear_terminal
from data.pycard_define import BattlePhase
from card.base_card import BaseCard
from utils.logger import Logger


class TutorialBattle2(BaseBattle):

    def initialize_battle(self):
        clear_terminal()
        print("初始化对战")
        self.player1.card_manager.hand.append(BaseCard.from_json(self.player1, "mw01_0003"))
        self.player2.card_manager.hand.append(BaseCard.from_json(self.player2, "mw01_0005"))

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
                    print(f"\t{color_text('教程:','yellow')} \"先手\"条件, 要求 卡牌在对手卡牌之前的时刻结算")
                    print(
                        f"\t{color_text('教程:','yellow')} {color_text('输入 [1] 并按回车键','yellow')}, 打出手牌中的 \"先发制人\""
                    )
                if self.round_cnt == 1 and self.turn_cnt == 2:
                    print(f"\t{color_text('教程:','yellow')} 角色的 架势 记录了角色上一回合出牌的 卡牌类型")
                    print(f"\t{color_text('教程:','yellow')} \"切换\"条件, 要求 卡牌类型 与 你当前的架势 不同")
                    print(
                        f"\t{color_text('教程:','yellow')} {color_text('输入 [1] 并按回车键','yellow')}, 打出手牌中的 \"翻滚\""
                    )
                if self.round_cnt == 1 and self.turn_cnt == 3:
                    print(f"\t{color_text('教程:','yellow')} 为了展示 \"撤离\" 的效果, 手动将 你的体力 设置为 0")
                    self.player1.character.ep.set_value(0)
                    print(f"\t{color_text('教程:','yellow')} 在 没有体力 或 没有手牌 的情况下, 可以考虑打出 \"撤离\"")
                    print(
                        f"\t{color_text('教程:','yellow')} \"挥砍\", \"翻滚\", \"撤离\" 都是 基础卡牌, 会常驻在手牌中"
                    )
                    print(
                        f"\t{color_text('教程:','yellow')} {color_text('输入 [3] 并按回车键','yellow')}, 打出手牌中的 \"撤离\""
                    )
                if self.round_cnt == 2 and self.turn_cnt == 1:
                    print(f"\t{color_text('教程:','yellow')} 你已经完成了当前教程的内容, 请尝试击败对手")

                for player in self.player_list:
                    self.play_phase(player)
                clear_terminal()

                # 结算阶段
                self.current_phase = BattlePhase.RESOLVE_PHASE
                self.resolve_phase()
                # 回合 1
                if self.round_cnt == 1 and self.turn_cnt == 1:
                    self.player1.card_manager.hand.append(BaseCard.from_json(self.player1, "sw01_0001"))
                    self.player2.card_manager.hand.append(BaseCard.from_json(self.player2, "mw01_0002"))
                # 回合 2
                if self.round_cnt == 1 and self.turn_cnt == 2:
                    self.player1.card_manager.hand = []
                    self.player1.card_manager.hand.append(BaseCard.from_json(self.player1, "mw01_0001"))
                    self.player1.card_manager.hand.append(BaseCard.from_json(self.player1, "sw01_0001"))
                    self.player1.card_manager.hand.append(BaseCard.from_json(self.player1, "sw01_0002"))

                # 回合结束
                self.end_turn()
                if self.round_cnt == 1 and self.turn_cnt == 1:
                    print(f"\t{color_text('教程:','yellow')} 满足 \"先手\"条件 后, \"先发制人\" 抵抗伤害的效果生效")
                if self.round_cnt == 1 and self.turn_cnt == 2:
                    print(f"\t{color_text('教程:','yellow')} 满足 \"切换\"条件 后, \"翻滚\" 使你获得了 \"闪避\"状态")
                    print(f"\t{color_text('教程:','yellow')} \"闪避\"状态下, 角色不再受到 对手出牌 的效果结算")
                if self.round_cnt == 1 and self.turn_cnt == 3:
                    print(
                        f"\t{color_text('教程:','yellow')} \"撤离\" 使你获得了 \"撤离\"状态, \"撤离\"状态 包含了闪避的效果"
                    )
                    print(f"\t{color_text('教程:','yellow')} 任意角色进入 \"撤离\"状态 , 双方进入 弃牌阶段,")

            # 弃牌阶段
            if not self.is_battle_over():
                input(color_text("输入回车键继续……", "gray"))
                clear_terminal()
                print(
                    f"\t{color_text('教程:','yellow')} {color_text('输入 [e] 并按回车键','yellow')}, 结束 弃牌阶段, 开始新一轮战斗"
                )
                self.current_phase = BattlePhase.DISCARD_PHASE
                for player in self.player_list:
                    self.discard_phase(player)
                input(color_text("输入回车键继续……", "gray"))
                clear_terminal()

            # 回合 3
            if self.round_cnt == 1 and self.turn_cnt == 3:
                self.player1.card_manager.deck.append(BaseCard.from_json(self.player1, "mw01_0003"))
                self.player1.card_manager.deck.append(BaseCard.from_json(self.player1, "mw01_0004"))
                self.player1.card_manager.deck.append(BaseCard.from_json(self.player1, "mw01_0005"))
                self.player2.card_manager.deck.append(BaseCard.from_json(self.player2, "mw01_0001"))
                self.player2.card_manager.deck.append(BaseCard.from_json(self.player2, "sw01_0001"))
                self.player2.card_manager.deck.append(BaseCard.from_json(self.player2, "sw01_0002"))

        return self.conclude_battle()

    def start_round(self):
        self.round_cnt += 1
        self.turn_cnt = 0
        print(f"---------------- 第 {self.round_cnt} 轮 ----------------")
        if self.round_cnt == 2:
            print(f"\t{color_text('教程:','yellow')} 每轮战斗的开始, 角色恢复体力和韧性, 清空延迟和状态, 补充手牌")
        for player in self.player_list:
            player.start_round()


if __name__ == "__main__":
    # 创建战斗实例
    battle = TutorialBattle2(["ch00001", "ch00001"])

    # 初始化战斗
    battle.initialize_battle()

    # 进入主循环
    battle.main_loop()
