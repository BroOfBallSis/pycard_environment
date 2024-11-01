from utils.draw_text import color_text, center_text, clear_terminal
from character.character_define import CharacterStatusType
from player.policy.base_policy import BasePolicy
import copy


class TerminalPolicy(BasePolicy):
    def __init__(self, player, policy_context):
        super().__init__(player, policy_context)

    def action_in_play_phase(self):
        # 返回出牌动作
        hand_card_index = self.get_command_from_console()
        return hand_card_index

    def display_hand(self) -> str:
        hand_str = []
        raw_hand = self.player.card_manager.hand
        for index, card in enumerate(raw_hand):
            # 根据体力显示能否打出卡牌
            if self.player.character.ep.value < card.ep_cost.real_value:
                index_color = "gray"
            else:
                index_color = "green"

            hand_str.append(f"{color_text(f'[{index}]', index_color)} {card}")
        print("\n".join(hand_str))

    def display_deck(self) -> str:
        # 深拷贝玩家的牌组
        temp_deck = copy.deepcopy(self.player.card_manager.deck)

        # 根据 card.name 对 temp_deck 进行排序
        temp_deck.sort(key=lambda card: card.card_id)

        # 打印排序后的牌组
        for card in temp_deck:
            print(card)

        del temp_deck

    def display_card_manager_with_command(self) -> str:
        # 使用 color_text 函数将命令显示为绿色
        card_manager_command_0 = f"{color_text('[q]', 'green')} " + center_text("查看牌堆", 12)
        card_manager_command_1 = f"{color_text('[w]', 'green')} " + center_text("出牌记录", 12)
        print(f"{card_manager_command_0} {card_manager_command_1}")

    def display_player(self, player):
        color_mapping = {
            "无": "gray",
            "风": "cyan",
            "火": "red",
            "山": "brown",  # 或者 "green"
            "林": "green",
            "阴": "purple",
            "雷": "yellow",
        }
        posture_str = player.posture.value
        posture_color = color_mapping[posture_str]
        print(f"{player.name}: {player.character}, 架势:{color_text(posture_str, posture_color)}\t{player.card_manager}")
        if player.character.statuses:
            print(f"  ∟ 状态: {', '.join(str(statu) for statu in player.character.statuses)}")

    def get_command_from_console(self) -> int:
        """
        从命令行获取出牌命令

        :return: 选择的手牌索引
        """
        self.display_player(self.player)
        self.display_player(self.player.opponent)
        self.display_card_manager_with_command()
        self.display_hand()
        while True:
            try:
                # 获取用户输入
                user_input = input("请输入指令: ")

                # 检查用户是否想要查看手牌
                if user_input.lower() == "q":
                    self.display_deck()
                    continue  # 继续循环，等待下一个输入

                # 尝试将输入转换为整数
                hand_index = int(user_input)

                temp_hand = self.player.card_manager.hand
                if 0 <= hand_index < len(temp_hand):
                    card_ep_cost = temp_hand[hand_index].ep_cost.real_value
                    if card_ep_cost > self.player.character.ep.value:
                        print(
                            color_text(
                                f"\t没有足够的体力(体力:{self.player.character.ep.value}, 费用:{card_ep_cost}), 请重新输入", "yellow"
                            )
                        )
                    else:
                        return hand_index
                else:
                    print(color_text(f"\t{hand_index} 不在手牌范围内([0 ~ {len(temp_hand)-1}]), 请重新输入", "yellow"))
            except ValueError:
                print(color_text(f"\t无效的索引, 请重新输入", "yellow"))
