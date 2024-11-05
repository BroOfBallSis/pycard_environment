from card.card_define import CardType
from player.policy.base_policy import BasePolicy
import random
from character.character_define import CharacterStatusType


class HammerPolicy(BasePolicy):
    def __init__(self, player, policy_context):
        super().__init__(player, policy_context)
        self.available_hand = {}

    def get_available_hand(self):
        self.available_hand = {}
        # 获取当前体力可用的手牌索引
        for i in range(len(self.player.card_manager.hand)):
            card_ep_cost = self.player.card_manager.hand[i].ep_cost.real_value
            if card_ep_cost <= self.player.character.ep.value:
                self.available_hand[i] = 0

    def auto_discard_phase(self, battle_info):
        discard_cnt = 0
        exist_card_ids = set()  # 使用集合提高查找效率
        card_index = 0

        while card_index < len(self.player.card_manager.hand):
            card_id = self.player.card_manager.hand[card_index].card_id
            if card_id in exist_card_ids:
                # 弃置重复的卡牌
                self.player.card_manager.discard_card_by_hand_index(card_index)
                discard_cnt += 1
                # 不增加 card_index，继续检查当前索引的卡牌
            else:
                exist_card_ids.add(card_id)  # 使用集合的 add 方法
                card_index += 1  # 只有在没有弃置时才增加索引

        self.player.logger.info(f"弃置 {discard_cnt} 张手牌", 1)

    def update_available_hand(self, priority_dict):
        for hand_index in self.available_hand:
            card_name = self.player.card_manager.hand[hand_index].name
            self.available_hand[hand_index] = max(self.available_hand[hand_index], priority_dict.get(card_name, 0))

    def action(self, battle_info):
        self.get_available_hand()
        self.get_priority_based_on_scenario()
        if self.available_hand:
            available_hand_str = ""
            for hand_index in self.available_hand:
                card_name = self.player.card_manager.hand[hand_index].name
                available_hand_str += f"{hand_index}:{card_name}({self.available_hand[hand_index]});\t"

            # print(f"sword_ai: {available_hand_str}")
            total_priority = sum(self.available_hand.values())
            if total_priority == 0:
                return random.choice(list(self.available_hand.keys()))

            # 按照概率随机采样
            weights = [self.available_hand[i] / total_priority for i in self.available_hand]
            selected_index = random.choices(list(self.available_hand.keys()), weights=weights, k=1)[0]
            return selected_index
        else:
            return 2

    def get_priority_based_on_scenario(self):
        character = self.player.character
        # 第1张出牌 或者 破绽后的出牌
        if self.player.posture == CardType.NONE:
            priority_dict = {
                "打击": 10,
                "格挡": 5,
                "撤离": 0,
                "前倾打击": 0,
                "顶盾撞击": 0,
                "侧身打击": 5,
                "重锤打击": 5,
                "下颚粉碎": 0,
                "重整旗鼓": 0,
                "生命药剂": 0,
                "便携手弩": 0,
            }
            if character.rp.value <= 2:
                priority_dict["重整旗鼓"] = 20

        # 有延迟时的出牌
        elif character.delay.value > 0:
            priority_dict = {
                "打击": 5,
                "格挡": 5,
                "撤离": 0,
                "前倾打击": 0,
                "顶盾撞击": 0,
                "侧身打击": 0,
                "重锤打击": 30,
                "下颚粉碎": 0,
                "重整旗鼓": 0,
                "生命药剂": 0,
                "便携手弩": 0,
            }
            if character.rp.value <= 2:
                priority_dict["重整旗鼓"] = 20
                priority_dict["格挡"] = 10
            elif self.player.posture == CardType.MOUNTAIN:
                priority_dict["顶盾撞击"] = 50

        # 没有延迟的出牌
        else:
            priority_dict = {
                "打击": 10,
                "格挡": 0,
                "撤离": 0,
                "前倾打击": 5,
                "顶盾撞击": 5,
                "侧身打击": 5,
                "重锤打击": 0,
                "下颚粉碎": 0,
                "重整旗鼓": 0,
                "生命药剂": 0,
                "便携手弩": 0,
            }
            if character.rp.value <= 2:
                priority_dict["重整旗鼓"] = 10
            if self.player.posture != CardType.WIND:
                priority_dict["前倾打击"] = 10
            if self.player.posture != CardType.FIRE and self.player.opponent.character.delay.value >= 2:
                priority_dict["重锤打击"] = 50
            if self.player.opponent.character.rp.value <= 2:
                priority_dict["便携手弩"] = 50

        if character.hp.max_value - character.hp.value >= 10 and character.rp.value > 2:
            priority_dict["生命药剂"] = 10
        if self.player.posture == CardType.MOUNTAIN:
            priority_dict["顶盾撞击"] = 10
        if character.ep.value <= 6:
            priority_dict["撤离"] = 5
        if self.player.opponent.character.has_status(CharacterStatusType.SLOW) or self.player.opponent.character.rp.value <= 2:
            priority_dict["下颚粉碎"] = 50

        self.update_available_hand(priority_dict)
