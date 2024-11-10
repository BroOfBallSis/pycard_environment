import random
import json
import os
from typing import List, Dict, Any
from card.base_card import BaseCard
from utils.draw_text import center_text, color_text
from utils.logger import Logger


class CardManager:
    def __init__(self, player, card_list: List[str]) -> None:
        """
        初始化 CardManager

        :param card_list: 包含所有卡牌 ID 的列表
        """
        self.card_list = card_list
        self.player = player
        self.deck = []
        self.hand = []
        self.discard_pile = []
        self._initialize_deck()
        self.logger = Logger(self.player.name)

    def _initialize_deck(self) -> None:
        """初始化牌堆，将所有卡牌实例化并放入牌堆"""
        for card_id in self.card_list:
            card = BaseCard.from_json(self.player, card_id)
            if card.is_base:
                self.hand.append(card)
            else:
                self.deck.append(card)
        random.shuffle(self.deck)  # 洗牌

    def add_card(self, card_id):
        card = BaseCard.from_json(self.player, card_id)
        self.hand.append(card)

    def draw_card(self, n: int, hand_limit: int = 10) -> None:
        """
        从牌堆抽 n 张牌，且手牌总数不超过 hand_limit 张

        :param n: 要抽的牌数
        :param hand_limit: 手牌上限
        """
        self.logger.increase_depth()
        old_value = len(self.hand)
        for _ in range(n):
            if len(self.hand) >= hand_limit:
                break
            if not self.deck and self.discard_pile:
                self.shuffle_discard_pile_into_deck()
            if self.deck:
                self.hand.append(self.deck.pop())
            else:
                # print(f"牌堆和弃牌堆为空, 结束抽牌")
                break
        now_value = len(self.hand)
        right_value_str = f"{now_value} (max)" if now_value == hand_limit else f"{now_value}"
        self.logger.info(f"手牌数量: {old_value} ↑ {right_value_str}")
        self.logger.decrease_depth()

    def clear_temporary_card(self):
        """移除手牌中的临时卡牌"""
        to_remove_cards = [card for card in self.hand if card.temporary]

        for card in to_remove_cards:
            self.logger.increase_depth()
            self.logger.info(f"移除 {card.name}")
            self.hand.remove(card)
            self.logger.decrease_depth()

    def discard_played_card(self, card: BaseCard) -> None:
        self.logger.increase_depth()
        """将卡牌从手牌移到弃牌堆"""
        if not card.is_base and card in self.hand:
            self.hand.remove(card)
        if not card.consumable and not card.temporary and not card.is_base:
            self.discard_pile.append(card)
        elif card.consumable or card.temporary:
            self.logger.info(f"消耗 {card.name}")
        self.logger.decrease_depth()

    def discard_card_by_hand_index(self, hand_index) -> None:
        """将卡牌从手牌移到弃牌堆"""
        if 0 <= hand_index < len(self.hand):
            card = self.hand[hand_index]
            if card.is_base:
                self.logger.info(f"无法弃置 '基础' 卡牌: {card.name}\n")
            else:
                self.hand.remove(card)
                self.discard_pile.append(card)
                if self.player.policy_name == "terminal":
                    self.logger.info(f"弃置: {card.name}\n")
        else:
            print(color_text(f"\t无效的索引, 请重新输入", "yellow"))

    def shuffle_discard_pile_into_deck(self) -> None:
        """将弃牌堆的牌洗牌并放入牌堆"""
        random.shuffle(self.discard_pile)
        self.deck.extend(self.discard_pile)
        self.discard_pile.clear()

    def __str__(self) -> str:
        """返回 CardManager 的字符串表示，显示牌堆、手牌和弃牌堆的状态"""
        deck_str = f"牌堆({len(self.deck)})"
        hand_str = f"手牌({len(self.hand)})"
        discard_pile_str = f"弃牌堆({len(self.discard_pile)})"
        return f"{hand_str}, {deck_str}, {discard_pile_str}"


if __name__ == "__main__":
    card_manager = CardManager(["mw01_0001", "sw01_0001", "mw01_0001", "sw01_0001"])
    print(card_manager)
    card_manager.draw_card(2)
    print(card_manager)
    card_manager.discard_card_by_hand_index(0)
    print(card_manager)
    card_manager.draw_card(3)
    print(card_manager)
