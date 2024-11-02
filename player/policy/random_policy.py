from player.policy.base_policy import BasePolicy
import random


class RandomPolicy(BasePolicy):
    def __init__(self, player, policy_context):
        super().__init__(player, policy_context)

    def action(self, battle_info):
        available_hand_index = []
        # 获取当前体力可用的手牌索引
        for i in range(len(self.player.card_manager.hand)):
            card_ep_cost = self.player.card_manager.hand[i].ep_cost.real_value
            if card_ep_cost <= self.player.character.ep.value:
                available_hand_index.append(i)

        # 如果有可用的手牌索引, 随机抽取一个
        if available_hand_index:
            selected_index = random.choice(available_hand_index)
            return selected_index
        else:
            print(f"\t{self.player.name} 没有可用的手牌")
            return -1
