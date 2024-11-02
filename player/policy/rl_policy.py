from player.policy.base_policy import BasePolicy
import random


class RLPolicy(BasePolicy):
    def __init__(self, player, policy_context):
        super().__init__(player, policy_context)

    def action(self, battle_info):
        # 返回出牌动作
        hand_card_index = random.randint(0, len(self.player.card_manager.hand) - 1)
        return hand_card_index
