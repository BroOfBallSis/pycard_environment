from enum import Enum
from player.base_player import BasePlayer
from character.status.base_status import CharacterStatusType
import time
from utils.draw_text import center_text, color_text, clear_terminal
from utils.debug import print_memory_info
from data.pycard_define import BattlePhase, character_to_policy
from utils.logger import Logger


class BaseBattle:
    def __init__(self, players, characters):
        self.player1 = BasePlayer(players[0], 1, characters[0], "terminal", self)
        enemy_ai = character_to_policy[characters[1]]
        self.player2 = BasePlayer(players[1], 2, characters[1], enemy_ai, self)
        self.player_list = [self.player1, self.player2]
        self.player1.opponent = self.player2
        self.player2.opponent = self.player1
        self.is_first_round = True
        self.round_cnt = 0
        self.turn_cnt = 0
        self.current_phase = BattlePhase.INITIALIZATION
        self.logger = Logger("battle")

    def initialize_battle(self):
        clear_terminal()
        print("初始化对战")

    def main_loop(self):
        while not self.is_battle_over():

            # 轮开始
            self.start_round(add_discard=True)

            while not self.is_round_over() and not self.is_battle_over():
                clear_terminal(confirm=True)

                # 回合开始
                self.start_turn()

                # 出牌阶段
                self.current_phase = BattlePhase.PLAY_PHASE
                for player in self.player_list:
                    self.play_phase(player)
                clear_terminal()

                # 结算阶段
                self.current_phase = BattlePhase.RESOLVE_PHASE
                self.resolve_phase()

                # 回合结束
                self.end_turn()

            # 弃牌阶段
            if not self.is_battle_over():
                clear_terminal(confirm=True)
                self.current_phase = BattlePhase.DISCARD_PHASE
                for player in self.player_list:
                    self.discard_phase(player)
                clear_terminal(confirm=True)

        return self.conclude_battle()

    def start_round(self, add_discard=False):
        self.round_cnt += 1
        self.turn_cnt = 0
        print(f"---------------- 第 {self.round_cnt} 轮 ----------------")
        self.logger.log_to_file(f"---------------- 第 {self.round_cnt} 轮 ----------------")
        for player in self.player_list:
            player.start_round()

        # 第 1 轮, 增加 弃牌阶段
        if self.is_first_round and add_discard:
            clear_terminal(confirm=True)
            self.is_first_round = False
            self.current_phase = BattlePhase.DISCARD_PHASE
            for player in self.player_list:
                self.discard_phase(player)
                player_hand_limit = player.character.hand_limit.value
                player.card_manager.draw_card(player_hand_limit, player_hand_limit)

    def start_turn(self):
        self.turn_cnt += 1
        print(f"---------------- 开 始 阶 段 ( 第 {self.round_cnt} 轮 - 第 {self.turn_cnt} 回 合 ) ----------------")
        self.logger.log_to_file(
            f"---------------- 开 始 阶 段 ( 第 {self.round_cnt} 轮 - 第 {self.turn_cnt} 回 合 ) ----------------"
        )
        for player in self.player_list:
            player.start_turn()
            self.logger.log_to_file(
                f"{player.name}: {player.character}, 架势:{player.posture.value}\t{player.card_manager}"
            )

    def play_phase(self, player: BasePlayer):
        command = player.get_action(self.get_battle_info())
        player.play_card_by_hand_index(command)

    def players_evaluate_and_update_status(self):
        for player in self.player_list:
            player.character.evaluate_and_update_status()
            player.update_hand()

    def resolve_character_status(self):
        for player in self.player_list:
            for status in player.character.statuses:
                status.on_resolve()

    def resolve_card_effects(self, player_list, immediate=False, end=False):
        if immediate:
            print(f"\n开 始:")
            self.resolve_character_status()
        elif end:
            print(f"结 束:")
        else:
            print(f"时 刻 {player_list[0].current_card.time_cost.real_value} :")

        # 结算同步效果
        for priority in range(10):
            context = {"priority": priority, "immediate": immediate, "end": end}
            for player in player_list:
                player.resolve_card_effect(context)

        self.players_evaluate_and_update_status()

    def resolve_asynchronous_card_effects(self, first_player: BasePlayer = None, later_player: BasePlayer = None):
        # 结算异步效果
        if first_player:
            self.resolve_card_effects([first_player])
            self.resolve_card_effects([later_player])
        else:
            self.resolve_card_effects(self.player_list)

    def resolve_phase(self):
        print(f"---------------- 结 算 阶 段 ( 第 {self.round_cnt} 轮 - 第 {self.turn_cnt} 回 合 ) ----------------")
        for player in self.player_list:
            print(f"{player.name_with_color}: {player.character}, 架势:{player.posture.value}\t{player.card_manager}")
            if player.character.statuses:
                print(f"  ∟ 状态: {', '.join(str(statu) for statu in player.character.statuses)}")
        print("\n出 牌:")
        for player in self.player_list:
            print(f"{player.name_with_color} : {player.current_card}")
            self.logger.log_to_file(f"{player.name} : {player.current_card}")

        self.resolve_card_effects(self.player_list, immediate=True)
        card_1_time_cost = self.player1.current_card.time_cost.real_value
        card_2_time_cost = self.player2.current_card.time_cost.real_value
        first_player, later_player = (
            (self.player1, self.player2)
            if card_1_time_cost < card_2_time_cost
            else (self.player2, self.player1) if card_1_time_cost > card_2_time_cost else (None, None)
        )
        self.resolve_asynchronous_card_effects(first_player, later_player)
        self.resolve_card_effects(self.player_list, end=True)

    def end_turn(self):
        real_value_1 = self.player1.current_card.time_cost.real_value
        real_value_2 = self.player2.current_card.time_cost.real_value
        base_delay = min(real_value_1, real_value_2)
        for player in self.player_list:
            player.end_turn(base_delay)

    def discard_phase(self, player: BasePlayer):
        player.card_manager.clear_temporary_card()
        if player.policy_name == "terminal":
            while True:
                command = player.get_action(self.get_battle_info())
                if command < 0:
                    print(color_text(f"结束 弃牌阶段", "yellow"))
                    break
                else:
                    clear_terminal()
                    player.discard_card_by_hand_index(command)
        else:
            player.auto_discard_phase(self.get_battle_info())

    def get_battle_info(self):
        return {
            "round_cnt": self.round_cnt,
            "turn_cnt": self.turn_cnt,
            "current_phase": self.current_phase,
        }

    def is_battle_over(self):
        return not self.player1.character.is_alive() or not self.player2.character.is_alive()

    def is_round_over(self):
        return self.player1.character.has_status(CharacterStatusType.RETREAT) or self.player2.character.has_status(
            CharacterStatusType.RETREAT
        )

    def conclude_battle(self):
        winner = self.player1 if not self.player2.character.is_alive() else self.player2
        print(f"{winner.opponent.name_with_color} has been defeated! {winner.name_with_color} wins!")
        clear_terminal(confirm=True)
        return winner is self.player1


if __name__ == "__main__":
    # 创建战斗实例
    battle = BaseBattle(["ch00001", "ch00001"])

    # 初始化战斗
    battle.initialize_battle()

    # 进入主循环
    battle.main_loop()
