# /player/base_player.py

from character.base_character import BaseCharacter
from data.pycard_define import CharacterStatusType, CharacterAttributeType
from data.character import character_library_instance
from card.card_manager import CardManager
from card.base_card import BaseCard
from data.pycard_define import CardType
from utils.draw_text import center_text, color_text
from data.pycard_define import PolicyType
import copy
from utils.logger import Logger
import gc
from data.pycard_define import BattlePhase
from player.policy.base_policy import PolicyFactory


class BasePlayer:
    def __init__(self, name, camp, character_id, policy, scene):
        self.name = center_text(name, 8)
        self.name_with_color = color_text(self.name, "blue" if camp == 1 else "red")
        self.camp = camp
        policy_context = None
        self.policy = PolicyFactory.create_policy(self, policy, policy_context)
        self.policy_name = policy
        self.opponent = None
        self.scene = scene
        self.logger = Logger(self.name)
        self.logger.set_source_name(self.name_with_color)

        # 根据 character_id 加载角色
        self.character = BaseCharacter.from_json(self, character_library_instance.get_character_info(character_id))

        # 根据角色的卡牌初始化 card_manager 的牌堆
        self.card_manager = CardManager(self, self.character.cards)
        self.previous_card_id = None
        self.current_card = None
        self.posture = CardType.NONE
        self.round_info = {}

    def play_card_by_hand_index(self, hand_index) -> BaseCard:
        if hand_index == -1:
            self.current_card = BaseCard.from_json(self, "flaws")
        elif 0 <= hand_index < len(self.card_manager.hand):
            self.current_card = self.card_manager.hand[hand_index]
        else:
            raise IndexError("无效的手牌索引")

    def discard_card_by_hand_index(self, hand_index) -> BaseCard:
        if 0 <= hand_index < len(self.card_manager.hand):
            self.card_manager.discard_card_by_hand_index(hand_index)
        else:
            print(color_text(f"\t无效的索引, 请重新输入", "yellow"))

    def resolve_card_effect(self, context):
        player_card = self.current_card
        player_card.play(self, self.opponent, context)

    def start_round(self):
        self.logger.set_depth(0)
        round_info_str = ""
        for attr in [CharacterAttributeType.HP, CharacterAttributeType.EP, CharacterAttributeType.RP]:
            if attr in self.round_info:
                round_info_str += f"{attr.value}: {self.round_info[attr]}, "
        if round_info_str:
            self.logger.info(f"{self.name_with_color}: 上轮统计: {round_info_str}")
        # 角色恢复韧性、体力、延迟
        self.character.start_round()
        self.posture = CardType.NONE
        del self.round_info
        self.round_info = {}

        # 补充手牌至上限
        self.card_manager.draw_card(self.character.hand_limit.value, self.character.hand_limit.value)

    def start_turn(self):
        self.character.start_turn()
        self.policy.start_turn()
        self.logger.set_depth(0)

        for _, card in enumerate(self.card_manager.hand):
            for condition in card.conditions:
                condition.reset()

    def end_turn(self, base_delay):
        if self.current_card:
            # 弃牌
            self.card_manager.discard_played_card(self.current_card)
            # 支付体力
            self.character.ep.decrease(self.current_card.ep_cost.real_value)
            # 计算延迟
            turn_delay = max(self.current_card.time_cost.real_value - base_delay, 0)
            self.character.delay.set_value(turn_delay)
            self.character.check_flaws_status()
            # 记录上一张卡牌
            self.posture = self.current_card.card_type
            self.previous_card_id = self.current_card.card_id

            # 清空当前卡牌
            self.current_card.temporary_condition.effects = []
            self.current_card = None
        self.policy.end_turn()

    def update_hand(self):
        raw_hand = self.card_manager.hand
        for index, card in enumerate(raw_hand):
            card.clear_mod()

            # 根据延迟调整卡牌的时间消耗
            card.time_cost.increase_mod(self.character.delay.value)

        if self.current_card:
            self.current_card.clear_mod()

            # 根据延迟调整卡牌的时间消耗
            self.current_card.time_cost.increase_mod(self.character.delay.value)

    def get_action(self, battle_info):
        current_phase = battle_info["current_phase"]
        # 更新手牌信息
        self.update_hand()

        # 拥有破绽, 跳过出牌
        flaws_status = self.character.has_status(CharacterStatusType.FLAWS)
        if flaws_status and current_phase == BattlePhase.PLAY_PHASE:
            return -1

        # 通过策略获取出牌索引
        hand_index = self.policy.action(battle_info)

        if current_phase == BattlePhase.PLAY_PHASE:
            # 检查出牌索引是否合法
            if isinstance(hand_index, int) and 0 <= hand_index < len(self.card_manager.hand):
                card_ep_cost = self.card_manager.hand[hand_index].ep_cost.real_value

                # 检查是否有足够的体力
                if card_ep_cost > self.character.ep.value:
                    print(color_text(f"\t{self.name} 体力不足, 视为打出 '破绽'", "red"))
                    return -1

                # 合法的出牌索引
                return hand_index
            else:
                # print(color_text(f"\t{self.name} 非法动作, 视为打出 '破绽'", "red"))
                return -1
        else:
            return hand_index

    def auto_discard_phase(self, battle_info):
        self.policy.auto_discard_phase(battle_info)

    def __str__(self) -> str:
        return f"Player: {self.player_name}, Camp: {self.camp}, Character: {self.character}"


if __name__ == "__main__":
    player = BasePlayer("hello", 0, "ch00001", None)
    print(player)
    print(player.character)
    print(player.card_manager)
    player.start_round()
    player.character.ep.set_value(3)
    player.character.delay.set_value(2)
    while True:
        player.start_turn()
        command = player.get_command_from_console()
        player.play_card_by_hand_index(command)
        card = player.current_card
        print(card)
        player.resolve_card_effect(card, player, card, 1)
        player.end_turn()
