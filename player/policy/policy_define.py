from enum import Enum
from player.policy.base_policy import BasePolicy
from player.policy.remote_policy import RemotePolicy
from player.policy.random_policy import RandomPolicy
from player.policy.rl_policy import RLPolicy
from player.policy.terminal_policy import TerminalPolicy
from player.policy.ai_policy.sword_ai_policy import SwordPolicy


class PolicyType(Enum):
    BASE = BasePolicy
    RANDOM = RandomPolicy
    REMOTE = RemotePolicy
    RL = RLPolicy
    TERMINAL = TerminalPolicy
    SWORD_AI = SwordPolicy


class PolicyFactory:
    @staticmethod
    def create_policy(player, policy_type_str, policy_context):
        # 将 policy_type_str 转换为大写，以便与枚举类型匹配
        policy_type_upper = policy_type_str.upper()

        if policy_type_upper in PolicyType.__members__:
            policy_type = PolicyType[policy_type_upper]
            return policy_type.value(player, policy_context)
        raise ValueError(f"Unsupported policy type: {policy_type_str}")
