from utils.draw_text import color_text, center_text, clear_terminal, display_help
from data.pycard_define import CharacterStatusType
from player.policy.base_policy import BasePolicy
import copy
from data.pycard_define import BattlePhase, card_type_color_mapping


class TerminalPolicy(BasePolicy):
    def __init__(self, player, policy_context):
        super().__init__(player, policy_context)

    def action(self, battle_info):
        # 返回出牌动作
        hand_card_index = self.get_command_from_console(battle_info)
        return hand_card_index

    def display_hand(self, current_phase) -> str:
        hand_str = []
        raw_hand = self.player.card_manager.hand
        for index, card in enumerate(raw_hand):
            # 根据体力显示能否打出卡牌
            if current_phase == BattlePhase.DISCARD_PHASE:
                index_color = "yellow"
            elif current_phase == BattlePhase.PLAY_PHASE:
                if self.player.character.ep.value < card.ep_cost.real_value:
                    index_color = "gray"
                else:
                    index_color = "green"
            hand_str.append(f"--------------------------------------------------------------")
            hand_str.append(f"{color_text(f'[{index+1}]', index_color)} {card.get_colored_str()}")
            # hand_str.append(f"{color_text(f'[{index+1}]', index_color)} {card.get_colored_str()}")
        print("\n".join(hand_str))

    def display_deck(self) -> str:
        # 使用切片创建玩家牌组的副本
        temp_deck = self.player.card_manager.deck[::]

        # 根据 card.card_id 对 temp_deck 进行排序
        temp_deck.sort(key=lambda card: card.card_id)

        # 打印排序后的牌组
        for card in temp_deck:
            print(card)

        del temp_deck

    def display_card_manager_with_command(self, phase_color) -> str:
        card_manager_command_0 = f"{color_text('[q]', phase_color)} {center_text('查看牌堆', 12)}"
        card_manager_command_1 = f"{color_text('[教程]', phase_color)} {center_text('输入关键字, 查看对应说明', 12)}"
        print(f"{card_manager_command_0} {card_manager_command_1}")

    def display_player(self, player):
        posture_str = player.posture.value
        posture_color = card_type_color_mapping[posture_str]
        print(
            f"{player.name_with_color}: {player.character}, 架势:{color_text(posture_str, posture_color)}\t{player.card_manager}"
        )
        if player.character.statuses:
            print(f"  ∟ 状态: {', '.join(str(statu) for statu in player.character.statuses)}")

    def get_command_from_console(self, battle_info) -> int:
        """
        从命令行获取出牌命令

        :return: 选择的手牌索引
        """
        current_phase = battle_info["current_phase"]
        phase_color = "green"
        if current_phase == BattlePhase.DISCARD_PHASE:
            phase_color = "yellow"
        current_phase_str = color_text(current_phase.value, phase_color)
        print(
            f"---------------- {current_phase_str} ( 第 {battle_info['round_cnt']} 轮 - 第 {battle_info['turn_cnt']} 回 合 )----------------"
        )
        self.display_player(self.player)
        self.display_player(self.player.opponent)
        self.display_card_manager_with_command(phase_color)
        self.display_hand(current_phase)
        while True:
            try:
                # 获取用户输入
                if current_phase == BattlePhase.DISCARD_PHASE:
                    print(f"{color_text('[e]', phase_color)} {center_text('结束弃牌', 12)}")
                user_input = input(f"'{current_phase_str}' 请输入指令: ")

                # 检查用户是否想要查看手牌
                if user_input.lower() == "q":
                    self.display_deck()
                    continue  # 继续循环，等待下一个输入

                # 检查用户是否想要查看教程
                if display_help(user_input):
                    continue  # 继续循环，等待下一个输入

                # 检查用户是否想要结束弃牌
                if user_input.lower() == "e" and current_phase == BattlePhase.DISCARD_PHASE:
                    return -1

                # 尝试将输入转换为整数
                hand_index = int(user_input) - 1

                temp_hand = self.player.card_manager.hand
                if 0 <= hand_index < len(temp_hand):
                    card_ep_cost = temp_hand[hand_index].ep_cost.real_value
                    if current_phase == BattlePhase.PLAY_PHASE and card_ep_cost > self.player.character.ep.value:
                        print(
                            color_text(
                                f"\t没有足够的体力(体力:{self.player.character.ep.value}, 费用:{card_ep_cost}), 请重新输入",
                                "yellow",
                            )
                        )
                    else:
                        return hand_index
                else:
                    print(color_text(f"\t{hand_index+1} 不在手牌范围内([1 ~ {len(temp_hand)}]), 请重新输入", "yellow"))
            except ValueError:
                print(color_text(f"\t无效的索引, 请重新输入", "yellow"))
