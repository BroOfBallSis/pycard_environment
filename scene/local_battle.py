from enum import Enum
from player.base_player import BasePlayer
from character.status.base_status import CharacterStatusType
import time
from utils.draw_text import color_text, clear_terminal
from utils.debug import print_memory_info


class BattlePhase(Enum):
    INITIALIZATION = "initialization"
    PLAY_PHASE = "play_phase"
    RESOLVE_PHASE = "resolve_phase"
    END_TURN = "end_turn"
    DISCARD_PHASE = "discard_phase"
    CONCLUDE = "conclude"


class Battle:
    def __init__(self):
        self.player1 = BasePlayer("player1", 1, "ch00001", "terminal", self)
        self.player2 = BasePlayer("player2", 2, "ch00001", "sword_ai", self)
        self.player_list = [self.player1, self.player2]
        self.player1.opponent = self.player2
        self.player2.opponent = self.player1
        self.round_cnt = 0
        self.turn_cnt = 0
        self.current_phase = BattlePhase.INITIALIZATION

    def initialize_battle(self):
        clear_terminal()
        print("初始化对战")

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
                print(
                    f"---------------- 出 牌 阶 段 ( 第 {self.round_cnt} 轮 - 第 {self.turn_cnt} 回 合 )----------------"
                )
                for player in self.player_list:
                    self.play_phase(player)

                # 结算阶段
                print(
                    f"---------------- 结 算 阶 段 ( 第 {self.round_cnt} 轮 - 第 {self.turn_cnt} 回 合 )----------------"
                )
                self.resolve_phase()

                # 回合结束
                self.end_turn()

            # 弃牌阶段
            for player in self.player_list:
                self.discard_phase(player)

            if not self.is_battle_over():
                input(color_text("输入回车键继续……", "gray"))
                clear_terminal()

        self.conclude_battle()

    def start_round(self):
        self.round_cnt += 1
        self.turn_cnt = 0
        print(f"---------------- 第 {self.round_cnt} 轮 ----------------")
        for player in self.player_list:
            player.start_round()

    def start_turn(self):
        # 关注内存占用情况
        print_memory_info()

        self.turn_cnt += 1
        print(f"---------------- 开 始 阶 段 ( 第 {self.round_cnt} 轮 - 第 {self.turn_cnt} 回 合 )----------------")
        for player in self.player_list:
            player.start_turn()

    def play_phase(self, player):
        command = player.get_action_in_play_phase()
        player.play_card_by_hand_index(command)

    def players_evaluate_and_update_status(self):
        for player in self.player_list:
            player.character.evaluate_and_update_status()
            player.update_hand()

    def resolve_synchronous_card_effects(self, immediate=False, end=False):
        # 结算同步效果
        for priority in range(10):
            context = {"priority": priority, "immediate": immediate, "end": end}
            for player in self.player_list:
                player.resolve_card_effect(context)
            self.players_evaluate_and_update_status()

    def resolve_asynchronous_card_effects(self, first_player=None, later_player=None):
        # 结算异步效果
        if first_player:
            print(f"时 刻 {first_player.current_card.time_cost.real_value} :")
            for priority in range(10):
                first_player.resolve_card_effect({"priority": priority})
            self.players_evaluate_and_update_status()

            print(f"时 刻 {later_player.current_card.time_cost.real_value} :")
            for priority in range(10):
                later_player.resolve_card_effect({"priority": priority})
            self.players_evaluate_and_update_status()

        else:
            print(f"时 刻 {self.player1.current_card.time_cost.real_value} :")
            self.resolve_synchronous_card_effects()

    def resolve_phase(self):
        for player in self.player_list:
            print(f"{player.name} : {player.current_card}")

        # 执行 priority 为 0 的效果，如(立即)的效果
        print(f"开 始:")
        self.resolve_synchronous_card_effects(immediate=True)

        # 执行 priority 为 1 的效果
        card_1_time_cost = self.player1.current_card.time_cost.real_value
        card_2_time_cost = self.player2.current_card.time_cost.real_value
        first_player = None
        later_player = None
        if card_1_time_cost < card_2_time_cost:
            first_player = self.player1
            later_player = self.player2
        elif card_1_time_cost > card_2_time_cost:
            first_player = self.player2
            later_player = self.player1
        self.resolve_asynchronous_card_effects(first_player, later_player)

        print(f"结 束:")
        self.resolve_synchronous_card_effects(end=True)

    def end_turn(self):
        base_delay = min(self.player1.current_card.time_cost.real_value, self.player2.current_card.time_cost.real_value)
        for player in self.player_list:
            player.end_turn(base_delay)

    def discard_phase(self, player):
        pass
        # 这里添加弃牌阶段的逻辑

    def is_battle_over(self):
        return not self.player1.character.is_alive() or not self.player2.character.is_alive()

    def is_round_over(self):
        return self.player1.character.has_status(CharacterStatusType.WITHDRAW) or self.player2.character.has_status(
            CharacterStatusType.WITHDRAW
        )

    def conclude_battle(self):
        if not self.player1.character.is_alive():
            print(f"{self.player1.name} has been defeated! {self.player2.name} wins!")
        elif not self.player2.character.is_alive():
            print(f"{self.player2.name} has been defeated! {self.player1.name} wins!")


if __name__ == "__main__":
    # 创建战斗实例
    battle = Battle()

    # 初始化战斗
    battle.initialize_battle()

    # 进入主循环
    battle.main_loop()
