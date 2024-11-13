from data.pycard_define import CardType
from player.policy.base_policy import BasePolicy
import random


class SwordMasterPolicy(BasePolicy):
    def __init__(self, player, policy_context):
        super().__init__(player, policy_context)
        self.available_hand = {}
        print("SwordMasterPolicy")

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

        self.player.logger.info(f"弃置 {discard_cnt} 张手牌")

    def display_hands(self):
        hand_str = f"{self.player.name_with_color}: "
        # 获取当前体力可用的手牌索引
        for i in range(len(self.player.card_manager.hand)):
            hand_str += self.player.card_manager.hand[i].name + ", "
        print(hand_str)


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

            print(f"sword_master_ai: {available_hand_str}")
            total_priority = sum(self.available_hand.values())
            if total_priority == 0:
                return 2

            # 找到 self.available_hand 中的最大值
            max_value = max(self.available_hand.values())

            # 找到最大值的索引，如果有多个最大值，取索引靠前的
            selected_index = next(key for key, value in self.available_hand.items() if value == max_value)
            return selected_index
        else:
            return 2

    def get_priority_based_on_scenario(self):
        random_index = random.randint(1, 6)
        character = self.player.character
        print(f"random_index is {random_index}")

        if random_index in [1, 2]:
            #   如果延迟<=1, 打出 ['长剑上挑', '长剑突刺'(切换), '先发制人', '翻滚'(切换), '挥砍'];
            #   否则, 打出 ['保持戒备', '重整旗鼓(体力≤3)', '长剑突刺'(切换), '翻滚'(切换)];
            if character.delay.value <= 1:
                priority_dict = {
                    "先发制人": 3,
                    "长剑上挑": 5,
                    '挥砍': 1
                }
                if self.player.posture != CardType.FOREST and self.player.posture != CardType.NONE:
                    priority_dict['翻滚'] = 2
                # if self.player.posture != CardType.WIND and self.player.posture != CardType.NONE:
                priority_dict['长剑突刺'] = 4
            else:
                priority_dict = {
                    "保持戒备": 5,
                }
                if character.ep.value <= 3:
                    priority_dict['重整旗鼓'] = 4
                # if self.player.posture != CardType.WIND and self.player.posture != CardType.NONE:
                priority_dict['长剑突刺'] = 3
                if self.player.posture != CardType.FOREST and self.player.posture != CardType.NONE:
                    priority_dict['翻滚'] = 2
        else:
            # 4 × "进攻策略":
            #   如果韧性>2, 且延迟<=1, 打出['长剑竖劈'(切换), '长剑突刺'(切换), '先发制人', '翻滚'(切换), '挥砍'];
            #   否则打出['长剑突刺'(切换), '重整旗鼓(体力≤3)', '保持戒备', '翻滚'(切换)];
            if character.delay.value <= 1 and character.rp.value > 2:
                priority_dict = {
                    "先发制人": 3,
                    "挥砍": 1
                }
                if self.player.posture != CardType.FOREST and self.player.posture != CardType.NONE:
                    priority_dict['翻滚'] = 2
                # if self.player.posture != CardType.WIND and self.player.posture != CardType.NONE:
                priority_dict['长剑突刺'] = 4
                # if self.player.posture != CardType.FIRE and self.player.posture != CardType.NONE:
                priority_dict['长剑竖劈'] = 5
            else:
                priority_dict = {
                    "保持戒备": 3
                }
                if character.ep.value <= 3:
                    priority_dict['重整旗鼓'] = 4
                # if self.player.posture != CardType.WIND and self.player.posture != CardType.NONE:
                priority_dict['长剑突刺'] = 5
                if self.player.posture != CardType.FOREST and self.player.posture != CardType.NONE:
                    priority_dict['翻滚'] = 2
        self.update_available_hand(priority_dict)
