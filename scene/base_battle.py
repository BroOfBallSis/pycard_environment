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
            self.start_round()

            if self.is_first_round:
                input(color_text("输入回车键继续……", "gray"))
                clear_terminal()
                self.is_first_round = False
                self.current_phase = BattlePhase.DISCARD_PHASE
                for player in self.player_list:
                    self.discard_phase(player)
                    player_hand_limit = player.character.hand_limit.value
                    player.card_manager.draw_card(player_hand_limit, player_hand_limit)

            while not self.is_round_over() and not self.is_battle_over():

                input(color_text("输入回车键继续……", "gray"))
                clear_terminal()

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
                input(color_text("输入回车键继续……", "gray"))
                clear_terminal()
                self.current_phase = BattlePhase.DISCARD_PHASE
                for player in self.player_list:
                    self.discard_phase(player)
                input(color_text("输入回车键继续……", "gray"))
                clear_terminal()

        return self.conclude_battle()

    def start_round(self):
        self.round_cnt += 1
        self.turn_cnt = 0
        print(f"---------------- 第 {self.round_cnt} 轮 ----------------")
        self.logger.log_to_file(f"---------------- 第 {self.round_cnt} 轮 ----------------")
        for player in self.player_list:
            player.start_round()

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
        battle_info = {
            "round_cnt": self.round_cnt,
            "turn_cnt": self.turn_cnt,
            "current_phase": self.current_phase,
        }
        command = player.get_action(battle_info)
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

    def resolve_asynchronous_card_effects(self, first_player: BasePlayer = None, later_player: BasePlayer = None):
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
        print(f"---------------- 结 算 阶 段 ( 第 {self.round_cnt} 轮 - 第 {self.turn_cnt} 回 合 ) ----------------")
        for player in self.player_list:
            print(f"{player.name_with_color}: {player.character}, 架势:{player.posture.value}\t{player.card_manager}")
            if player.character.statuses:
                print(f"  ∟ 状态: {', '.join(str(statu) for statu in player.character.statuses)}")
        print("\n出 牌:")
        for player in self.player_list:
            print(f"{player.name_with_color} : {player.current_card}")
            self.logger.log_to_file(f"{player.name} : {player.current_card}")

        # 执行 priority 为 0 的效果，如(立即)的效果
        print(f"\n开 始:")
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
        real_value_1 = self.player1.current_card.time_cost.real_value
        real_value_2 = self.player2.current_card.time_cost.real_value
        base_delay = min(real_value_1, real_value_2)
        for player in self.player_list:
            player.end_turn(base_delay)

    def discard_phase(self, player: BasePlayer):
        battle_info = {
            "round_cnt": self.round_cnt,
            "turn_cnt": self.turn_cnt,
            "current_phase": self.current_phase,
        }
        player.card_manager.clear_temporary_card()
        if player.policy_name == "terminal":
            while True:
                command = player.get_action(battle_info)
                if command < 0:
                    print(color_text(f"结束 弃牌阶段", "yellow"))
                    break
                else:
                    clear_terminal()
                    player.discard_card_by_hand_index(command)
        else:
            player.auto_discard_phase(battle_info)

    def is_battle_over(self):
        return not self.player1.character.is_alive() or not self.player2.character.is_alive()

    def is_round_over(self):
        return self.player1.character.has_status(CharacterStatusType.RETREAT) or self.player2.character.has_status(
            CharacterStatusType.RETREAT
        )

    def conclude_battle(self):
        if not self.player1.character.is_alive():
            print(f"{self.player1.name} has been defeated! {self.player2.name} wins!")
            input(color_text("输入回车键继续……", "gray"))
            clear_terminal()
            return False
        elif not self.player2.character.is_alive():
            print(f"{self.player2.name} has been defeated! {self.player1.name} wins!")
            input(color_text("输入回车键继续……", "gray"))
            clear_terminal()
            return True


if __name__ == "__main__":
    # 创建战斗实例
    battle = BaseBattle(["ch00001", "ch00001"])

    # 初始化战斗
    battle.initialize_battle()

    # 进入主循环
    battle.main_loop()
