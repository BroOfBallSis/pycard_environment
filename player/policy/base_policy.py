from data.pycard_define import PolicyType
import importlib
from data.pycard_define import PolicyType


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


class PolicyFactory:
    @staticmethod
    def create_policy(player, policy_type_str, policy_context):
        # 将 policy_type_str 转换为大写，以便与枚举类型匹配
        policy_type_upper = policy_type_str.upper()

        if policy_type_upper in PolicyType.__members__:
            module_name, policy_class_name = PolicyType[policy_type_upper].value

            # 动态导入策略类
            module = importlib.import_module(f"player.policy.{module_name}")
            policy_class = getattr(module, policy_class_name)
            return policy_class(player, policy_context)

        raise ValueError(f"Unsupported policy type: {policy_type_str}")
