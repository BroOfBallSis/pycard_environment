class BasePolicy:
    def __init__(self, player, policy_context):
        self.player = player
        self.policy_context = policy_context

    def action(self, battle_info):
        raise NotImplementedError("子类必须实现 action 方法")

    def auto_discard_phase(self, battle_info):
        pass

    def start_turn(self):
        pass

    def end_turn(self):
        pass
