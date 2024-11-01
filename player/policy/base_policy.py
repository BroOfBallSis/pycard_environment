class BasePolicy:
    def __init__(self, player, policy_context):
        self.player = player
        self.policy_context = policy_context

    def action_in_play_phase(self):
        raise NotImplementedError("子类必须实现 action_in_play_phase 方法")

    def start_turn(self):
        pass

    def end_turn(self):
        pass
