# /player/base_player.py

from character.base_character import BaseCharacter
from character.character_define import CharacterStatusType, CharacterAttributeType
from data.character import character_library_instance
from card.card_manager import CardManager
from card.base_card import BaseCard
from card.card_define import CardType
from utils.draw_text import center_text, color_text
from player.policy.policy_define import PolicyFactory
import copy
from utils.logger import Logger
import gc


class BasePlayer:
    def __init__(self, name, camp, character_id, policy, scene):
        """
        初始化玩家基类

        :param name: 玩家名称
        :param camp: 阵营
        :param character_id: 控制的角色ID
        :param policy: 使用的策略
        """
        self.name = color_text(name, "blue" if camp == 1 else "red")
        self.camp = camp
        policy_context = None
        self.policy = PolicyFactory.create_policy(self, policy, policy_context)
        self.opponent = None
        self.scene = scene
        self.logger = Logger(self.name)

        # 根据 character_id 加载角色
        self.character = BaseCharacter.from_json(self, character_library_instance.get_character_info(character_id))

        # 根据角色的卡牌初始化 card_manager 的牌堆
        self.card_manager = CardManager(self, self.character.cards)
        self.previous_card_id = None
        self.current_card = None
        self.posture = CardType.NONE
        self.round_info = {}

    def play_card_by_hand_index(self, hand_index) -> BaseCard:
        """
        根据手牌索引出牌

        :param hand_index: 手牌索引
        :return: 出牌的卡牌实例
        """
        if hand_index == -1:
            self.current_card = BaseCard.from_json(self, "flaws")
        elif 0 <= hand_index < len(self.card_manager.hand):
            self.current_card = self.card_manager.hand[hand_index]
        else:
            raise IndexError("无效的手牌索引")

    def resolve_card_effect(self, context):
        """
        结算卡牌效果

        :param player_card: 自己的卡牌
        :param context: 上下文
        """
        player_card = self.current_card
        player_card.play(self, self.opponent, context)

    def start_round(self):
        """
        每轮对战开始时的操作
        """
        round_info_str = ""
        for attr in [CharacterAttributeType.HP, CharacterAttributeType.EP, CharacterAttributeType.RP]:
            if attr in self.round_info:
                round_info_str += f"{attr.value}: {self.round_info[attr]}, "
        if round_info_str:
            self.logger.info(f"上轮统计: {round_info_str}", 1)
        # 角色恢复韧性、体力、延迟
        self.character.start_round()
        self.posture = CardType.NONE
        del self.round_info
        self.round_info = {}

        # 补充手牌至上限
        self.card_manager.draw_cards(self.character.hand_limit.value, self.character.hand_limit.value)

    def start_turn(self):
        """
        每回合对战开始时的操作
        """
        self.character.start_turn()
        # 更新手牌信息
        self.update_hand()
        self.policy.start_turn()

    def end_turn(self, base_delay):
        """
        每回合对战结束时的操作
        """
        if self.current_card:
            # 弃牌
            self.card_manager.discard_card(self.current_card)
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
            self.current_card = None
        self.policy.end_turn()

    def update_hand(self):
        raw_hand = self.card_manager.hand
        for index, card in enumerate(raw_hand):
            card.clear_mod()

            # 根据延迟调整卡牌的时间消耗
            card.time_cost.increase_mod(self.character.delay.value)

            # 根据角色状态调整卡牌的属性
            # 根据角色的装备调整卡牌的属性

    def get_action_in_play_phase(self):
        # 拥有破绽, 跳过出牌
        flaws_status = self.character.has_status(CharacterStatusType.FLAWS)
        if flaws_status:
            flaws_status.decrease(1)
            return -1

        # 通过策略获取出牌索引
        hand_index = self.policy.action_in_play_phase()

        # 检查出牌索引是否合法
        if isinstance(hand_index, int) and 0 <= hand_index < len(self.card_manager.hand):
            card_ep_cost = self.card_manager.hand[hand_index].ep_cost.real_value

            # 检查是否有足够的体力
            if card_ep_cost > self.character.ep.value:
                print(color_text(f"\t{self.name} 体力不足, 视为打出 '破绽'", "red"))
                return -1

            return hand_index
        else:
            print(color_text(f"\t{self.name} 非法动作, 视为打出 '破绽'", "red"))
            return -1

    def __str__(self) -> str:
        """
        返回 BasePlayer 的字符串表示，显示玩家名称、阵营和角色信息
        """
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
